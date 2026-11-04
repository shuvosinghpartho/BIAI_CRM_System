from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True, index=True)
    source = Column(String(50), nullable=False)  # whatsapp / facebook / website / phone
    interest = Column(String(50), nullable=False, default="unknown")  # bootcamp / fellowship / corporate / unknown
    status = Column(String(50), nullable=False, default="New")  # New / Contacted / Interested / Paid / Lost
    enquiry_type = Column(String(50), nullable=False, default="sales")  # sales / support / spam / job_seeker
    language = Column(String(50), nullable=True)  # bangla / banglish / english
    message = Column(Text, nullable=False)
    ai_reply = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_contacted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "source": self.source,
            "interest": self.interest,
            "status": self.status,
            "enquiry_type": self.enquiry_type,
            "language": self.language,
            "message": self.message,
            "ai_reply": self.ai_reply,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_contacted_at": self.last_contacted_at.isoformat() if self.last_contacted_at else None,
        }

