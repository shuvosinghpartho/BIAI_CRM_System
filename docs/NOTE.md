# Project Note: BIAI CRM

**Author:** Antigravity AI Engineering  
**Project:** BIAI Admissions & Lead Pipeline CRM (Bangladesh)

---

### 1. What I Built
- **Backend (FastAPI + SQLite + APScheduler):**
  - Robust relational schema for enquiries tracking channel source, interest track, sales pipeline stages (`New`, `Contacted`, `Interested`, `Paid`, `Lost`), non-sales enquiry types (`support`, `spam`, `job_seeker`), and contact timestamps.
  - Automatic `last_contacted_at` tracking on status transitions to identify leads exceeding the 48-hour SLA.
  - Hybrid extraction engine combining deterministic rules (Bangla digit conversion, Bangladeshi phone regex, Bengali script detection, keyword markers) and Google Gemini LLM (`google-genai` SDK) for semantic reasoning.
  - Multi-language response generator matching the customer's communication language (English reply for English, Banglish reply for Bangla/Banglish).
  - Background scheduler running hourly checks for overdue enquiries.
  - Executive weekly analytics and AI intelligence reporting.

- **Frontend (Vue 3 + Vite + Pinia + Vue Router):**
  - Interactive 5-column Kanban pipeline board displaying only sales leads, with channel filters, full-text search, and quick status transition dropdowns.
  - Smart Enquiry Creator with instant AI extraction, editable fields, and a suggested reply box with one-click clipboard copying.
  - Dedicated "Other Enquiries" view to isolate support complaints, job applications, and promotional spam.
  - Executive Summary view with KPI metric cards, AI weekly summary, and an actionable list of overdue leads.

---

### 2. AI Tools & Techniques Used
- **Google GenAI SDK (`google-genai`):** Model invocation with structured JSON response generation (`types.GenerateContentConfig`).
- **Prompt Engineering:** Strict few-shot prompts covering edge cases (mixed-script Bengali/English, Banglish transliterations, informal WhatsApp messages).
- **Graceful Hybrid Fallback:** If Gemini experiences network errors or quota limits, the system seamlessly falls back to keyword/regex rules and structured bilingual response templates with zero app crashes.

---

### 3. Current Limitations / What Does Not Work Yet
- **Complex Mixed Intentions:** If a user combines multiple inquiries in one message (e.g., asking about both a bootcamp and a corporate training deal in the same sentence), the system defaults to the dominant track rather than splitting into two separate leads.
- **True Drag-and-Drop:** Per prompt specifications, pipeline status changes are executed via clean dropdown selects rather than HTML5 drag-and-drop.
- **Direct WhatsApp/Meta Webhooks:** Currently relies on pasting or CSV batch import rather than live webhook integrations with the Meta Cloud API.

---

### 4. Next Fixes & Roadmap
1. Connect live Meta WhatsApp Business Cloud API and Facebook Graph Webhooks for automated real-time ingestion.
2. Add multi-user role-based access control (RBAC) separating sales counselors from executive admins.
3. Add drag-and-drop support with optimistic UI updates in the pipeline board.
4. Implement automated WhatsApp follow-up messaging triggers when an enquiry reaches 48 hours without contact.
