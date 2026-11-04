from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class EnquiryBase(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    source: str
    interest: str = "unknown"
    status: str = "New"
    enquiry_type: str = "sales"
    language: Optional[str] = None
    message: str
    ai_reply: Optional[str] = None
    last_contacted_at: Optional[datetime] = None

class EnquiryCreate(EnquiryBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

class EnquiryUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    interest: Optional[str] = None
    status: Optional[str] = None
    enquiry_type: Optional[str] = None
    language: Optional[str] = None
    message: Optional[str] = None
    ai_reply: Optional[str] = None
    last_contacted_at: Optional[datetime] = None

class EnquiryResponse(EnquiryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

