import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import Enquiry
from app.services.reminder_service import get_overdue_enquiries
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "weekly_summary.txt"

# In-memory cache for weekly summary
_summary_cache: Dict[str, Any] = {
    "timestamp": 0.0,
    "data": None
}

def invalidate_summary_cache():
    """Call when an enquiry is added or updated so next summary reflects changes."""
    _summary_cache["timestamp"] = 0.0
    _summary_cache["data"] = None

def generate_weekly_summary(db: Session, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Compiles enquiry metrics and generates an AI summary.
    Caches the summary for 10 minutes so page transitions are instantaneous.
    Falls back to a structured template if AI service is unavailable.
    """
    current_time = time.time()
    if not force_refresh and _summary_cache["data"] and (current_time - _summary_cache["timestamp"] < 600):
        return _summary_cache["data"]

    enquiries = db.query(Enquiry).all()
    overdue_list = get_overdue_enquiries(db)

    # Basic stats
    total = len(enquiries)
    by_status = {}
    by_channel = {}
    by_interest = {}
    by_type = {}

    for e in enquiries:
        by_status[e.status] = by_status.get(e.status, 0) + 1
        by_channel[e.source] = by_channel.get(e.source, 0) + 1
        by_interest[e.interest] = by_interest.get(e.interest, 0) + 1
        by_type[e.enquiry_type] = by_type.get(e.enquiry_type, 0) + 1

    summary_stats = {
        "total_enquiries": total,
        "overdue_count": len(overdue_list),
        "status_breakdown": by_status,
        "channel_breakdown": by_channel,
        "interest_breakdown": by_interest,
        "type_breakdown": by_type,
    }

    # Format textual prompt
    data_context = (
        f"Total Enquiries: {total}\n"
        f"Overdue Follow-ups (>48h): {len(overdue_list)}\n"
        f"By Status: {json.dumps(by_status)}\n"
        f"By Channel: {json.dumps(by_channel)}\n"
        f"By Interest: {json.dumps(by_interest)}\n"
        f"By Enquiry Type: {json.dumps(by_type)}\n\n"
        "Sample Messages:\n" +
        "\n".join([f"- [{e.source.upper()}] ({e.interest}) {e.name or 'Anonymous'}: {e.message[:80]}" for e in enquiries[:10]])
    )

    ai_report = None
    if gemini_service.is_available() and PROMPT_FILE.exists():
        try:
            template = PROMPT_FILE.read_text(encoding="utf-8")
            prompt = template.format(enquiries_summary=data_context)
            ai_report = gemini_service.generate_text(prompt, max_tokens=500)
        except Exception as e:
            logger.warning(f"Failed to generate AI weekly summary: {e}")

    # Fallback template if AI call did not return text
    if not ai_report:
        ai_report = f"""### BIAI Weekly Executive CRM Summary

**Overview**
- Total Enquiries Processed: **{total}**
- Active Overdue Follow-ups (>48 hrs): **{len(overdue_list)}**

**Channel Performance**
- Most active sources: {", ".join([f"{k}: {v}" for k, v in by_channel.items()])}

**Program Interest**
- Bootcamp: {by_interest.get('bootcamp', 0)} enquiries
- Fellowship: {by_interest.get('fellowship', 0)} enquiries
- Corporate Training: {by_interest.get('corporate', 0)} enquiries
- General / Other: {by_interest.get('unknown', 0)} enquiries

**Pipeline Status**
- New: {by_status.get('New', 0)}, Contacted: {by_status.get('Contacted', 0)}, Interested: {by_status.get('Interested', 0)}, Paid: {by_status.get('Paid', 0)}, Lost: {by_status.get('Lost', 0)}

**Recommendations**
1. Immediately prioritize contacting the {len(overdue_list)} overdue leads.
2. WhatsApp and Facebook continue to drive majority enquiries; ensure quick response templates are active.
3. Schedule direct calls with corporate leads to finalize bespoke B2B contracts.
"""

    result = {
        "stats": summary_stats,
        "ai_summary": ai_report,
        "generated_at": datetime.utcnow().isoformat()
    }

    _summary_cache["timestamp"] = current_time
    _summary_cache["data"] = result
    return result
