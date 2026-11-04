from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.extractor import extract_enquiry_data
from app.services.reply_service import suggest_reply

router = APIRouter(prefix="/api/ai", tags=["ai"])

class ExtractRequest(BaseModel):
    message: str
    source: Optional[str] = None

class ExtractResponse(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    source: str
    interest: str
    enquiry_type: str
    language: str

class SuggestReplyRequest(BaseModel):
    message: str
    name: Optional[str] = None
    interest: Optional[str] = None
    enquiry_type: Optional[str] = None
    language: Optional[str] = None

class SuggestReplyResponse(BaseModel):
    reply: str

@router.post("/extract", response_model=ExtractResponse)
def api_extract(payload: ExtractRequest):
    data = extract_enquiry_data(payload.message, source=payload.source)
    return ExtractResponse(**data)

@router.post("/suggest-reply", response_model=SuggestReplyResponse)
def api_suggest_reply(payload: SuggestReplyRequest):
    reply_text = suggest_reply(
        message=payload.message,
        name=payload.name,
        interest=payload.interest,
        enquiry_type=payload.enquiry_type,
        language=payload.language
    )
    return SuggestReplyResponse(reply=reply_text)
