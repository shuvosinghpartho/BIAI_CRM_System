from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Enquiry
from app.schemas import EnquiryCreate, EnquiryUpdate, EnquiryResponse

router = APIRouter(prefix="/api/enquiries", tags=["enquiries"])

@router.post("", response_model=EnquiryResponse, status_code=201)
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    if "created_at" in data and data["created_at"] is None:
        data.pop("created_at")
    
    enquiry = Enquiry(**data)
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
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

    # Rule: set last_contacted_at when status changes unless explicitly specified
    if "status" in update_data and update_data["status"] != enquiry.status:
        if "last_contacted_at" not in update_data or update_data["last_contacted_at"] is None:
            update_data["last_contacted_at"] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(enquiry, key, value)

    db.commit()
    db.refresh(enquiry)
    return enquiry

@router.delete("/{enquiry_id}", status_code=204)
def delete_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    db.delete(enquiry)
    db.commit()
    return None

