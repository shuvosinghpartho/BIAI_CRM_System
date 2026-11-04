# BIAI CRM: Project Brief and Structure

Build a simple CRM for BIAI (Bangladesh).

## Problem
People contact BIAI via WhatsApp, Facebook, website and phone calls. Some enquiries get lost and nobody knows who needs a follow-up.

## Requirements
1. Save each enquiry: name, phone, source (channel), interest (bootcamp / fellowship / corporate / unknown), status.
2. AI reads a pasted message (Bangla, Banglish or English) and auto-fills those fields.
3. AI suggests a reply in English or Banglish, matching how the sender wrote.
4. Pipeline board with 5 statuses: New, Contacted, Interested, Paid, Lost.
5. Optional extras: highlight enquiries with no follow-up for 48 hours; weekly summary written by AI.

## Rules
- Use ONLY the sample data in data/sample-enquiries.csv (20 fictional enquiries, columns: id, channel, received at, sender name, phone, message). No real customer data.
- AI = Google Gemini free API via the `google-genai` Python SDK. Key in .env as GEMINI_API_KEY. Never hardcode or commit the key. Model name goes in config.py so it is easy to change.
- Hybrid extraction: rules first (phone regex, keywords), Gemini for the rest. If Gemini fails or is rate-limited, the app must still work using rules and reply templates (no crashes).
- Some samples are NOT sales (support issue, spam, job seeker). Classify each as enquiry_type: sales / support / spam / job_seeker. Only "sales" goes on the pipeline board. Others go to an "Other" page.
- Handle Bangla digits (০১৭...) by converting to English digits before phone matching. Normalize phones to 01XXXXXXXXX.
- Language detection: Bangla script -> "bangla"; Latin letters with Bangla words (kobe, koto, chai, ache, ami) -> "banglish"; else "english". Reply language: English if sender wrote English, Banglish if Bangla or Banglish.
- Keep the code simple and readable. I must be able to explain it and make small changes live.

