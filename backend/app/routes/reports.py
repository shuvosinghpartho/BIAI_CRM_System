from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EnquiryResponse
from app.services.reminder_service import get_overdue_enquiries
from app.services.summary_service import generate_weekly_summary

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/overdue", response_model=List[EnquiryResponse])
def get_overdue_reports(db: Session = Depends(get_db)):
    """
    Returns sales enquiries not in Paid/Lost with no follow-up for 48h+.
    """
    return get_overdue_enquiries(db)

@router.get("/weekly-summary")
def get_weekly_summary_report(
    refresh: bool = Query(False, description="Force AI re-generation ignoring cache"),
    db: Session = Depends(get_db)
):
    """
    Returns an AI-generated weekly CRM summary along with metrics.
    Cached for instant performance unless refresh=true is passed.
    """
    return generate_weekly_summary(db, force_refresh=refresh)
