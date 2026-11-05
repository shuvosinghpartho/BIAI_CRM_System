from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Enquiry
from app.schemas import EnquiryCreate, EnquiryUpdate, EnquiryResponse
from app.services.summary_service import invalidate_summary_cache

router = APIRouter(prefix="/api/enquiries", tags=["enquiries"])

@router.post("", response_model=EnquiryResponse, status_code=201)
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    if "created_at" in data and data["created_at"] is None:
        data.pop("created_at")
    
    # Clean whitespace
    if "message" in data and isinstance(data["message"], str):
        data["message"] = data["message"].strip()
    if "name" in data and isinstance(data["name"], str):
        data["name"] = data["name"].strip() or None
    if "phone" in data and isinstance(data["phone"], str):
        data["phone"] = data["phone"].strip() or None

    # Validate non-empty content
    if not data.get("message") and not data.get("name") and not data.get("phone"):
        raise HTTPException(
            status_code=422,
            detail="Enquiry message or prospect contact details cannot be empty or whitespace."
        )

    if not data.get("message"):
        data["message"] = f"Direct enquiry for {data.get('name') or data.get('phone') or 'Prospect'}"

    # Anti-Spam / Idempotency Guard:
    # If identical enquiry (same message, phone, source) was received in the last 4 seconds,
    # return the already created enquiry instead of creating duplicate database rows from rapid button clicks.
    recent_threshold = datetime.utcnow() - timedelta(seconds=4)
    existing = db.query(Enquiry).filter(
        Enquiry.message == data["message"],
        Enquiry.phone == data.get("phone"),
        Enquiry.source == data.get("source"),
        Enquiry.created_at >= recent_threshold
    ).order_by(desc(Enquiry.created_at)).first()

    if existing:
        return existing

    enquiry = Enquiry(**data)
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    invalidate_summary_cache()
    return enquiry

@router.get("", response_model=List[EnquiryResponse])
def list_enquiries(
    status: Optional[str] = Query(None, description="Filter by status (New, Contacted, Interested, Paid, Lost)"),
    enquiry_type: Optional[str] = Query(None, description="Filter by enquiry type (sales, support, spam, job_seeker)"),
    source: Optional[str] = Query(None, description="Filter by source (whatsapp, facebook, website, phone)"),
    search: Optional[str] = Query(None, description="Search by name, phone, or message"),
    db: Session = Depends(get_db)
):
    query = db.query(Enquiry)
    if status:
        query = query.filter(Enquiry.status == status)
    if enquiry_type:
        query = query.filter(Enquiry.enquiry_type == enquiry_type)
    if source:
        query = query.filter(Enquiry.source == source)
    if search:
        term = f"%{search}%"
        query = query.filter(
            (Enquiry.name.ilike(term)) | 
            (Enquiry.phone.ilike(term)) | 
            (Enquiry.message.ilike(term))
        )
    return query.order_by(desc(Enquiry.created_at)).all()

@router.get("/{enquiry_id}", response_model=EnquiryResponse)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return enquiry

@router.patch("/{enquiry_id}", response_model=EnquiryResponse)
def update_enquiry(enquiry_id: int, payload: EnquiryUpdate, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    update_data = payload.model_dump(exclude_unset=True)

    # Clean whitespace on string fields
    for k in ["name", "phone", "message"]:
        if k in update_data and isinstance(update_data[k], str):
            update_data[k] = update_data[k].strip() or None

    # Rule: set last_contacted_at when status changes unless explicitly specified
    if "status" in update_data and update_data["status"] != enquiry.status:
        if "last_contacted_at" not in update_data or update_data["last_contacted_at"] is None:
            update_data["last_contacted_at"] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(enquiry, key, value)

    db.commit()
    db.refresh(enquiry)
    invalidate_summary_cache()
    return enquiry

@router.delete("/{enquiry_id}", status_code=204)
def delete_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    db.delete(enquiry)
    db.commit()
    invalidate_summary_cache()
    return None

