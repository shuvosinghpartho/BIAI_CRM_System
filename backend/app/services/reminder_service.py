from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.config import FOLLOWUP_HOURS
from app.models import Enquiry

def get_overdue_enquiries(db: Session) -> List[Enquiry]:
    """
    Returns sales enquiries not in Paid/Lost where:
    - (last_contacted_at is None and created_at < now - 48h) OR
    - (last_contacted_at < now - 48h)
    """
    cutoff = datetime.utcnow() - timedelta(hours=FOLLOWUP_HOURS)
    
    query = db.query(Enquiry).filter(
        Enquiry.enquiry_type == "sales",
        ~Enquiry.status.in_(["Paid", "Lost"]),
        or_(
            (Enquiry.last_contacted_at == None) & (Enquiry.created_at <= cutoff),
            (Enquiry.last_contacted_at <= cutoff)
        )
    ).order_by(Enquiry.created_at.asc())

    return query.all()

def is_enquiry_overdue(enquiry: Enquiry) -> bool:
    """Helper to check if a single enquiry is overdue."""
    if enquiry.enquiry_type != "sales" or enquiry.status in ["Paid", "Lost"]:
        return False
    
    cutoff = datetime.utcnow() - timedelta(hours=FOLLOWUP_HOURS)
    ref_time = enquiry.last_contacted_at or enquiry.created_at
    return ref_time <= cutoff
