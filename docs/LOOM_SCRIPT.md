# BIAI CRM — 5-Minute Loom Video Walkthrough Script

**Speaker:** Technical Lead / Full-Stack Engineer  
**Duration:** ~5:00 Minutes  
**Target Audience:** BIAI Leadership, Admissions Team, Evaluators

---

### [0:00 - 0:45] Introduction & The Problem
**Visual:** Show the problem statement and the BIAI CRM Pipeline Board loaded with 20 sample enquiries.

> "Hello everyone! Today, I’m excited to walk you through the custom CRM built specifically for BIAI (Bangladesh AI Institute).
>
> **The Problem:** Every week, hundreds of prospective students and enterprise clients reach out to BIAI through WhatsApp, Facebook Messenger, website forms, and phone calls. In the past, enquiries were written in a mix of Bangla, Banglish, and English. Some got buried, support complaints got mixed up with high-value corporate deals, and nobody had visibility into which leads were left hanging without a follow-up for 48 hours.
>
> We built this system to solve that exact problem — combining deterministic rule-based speed with Google Gemini AI intelligence."

---

### [0:45 - 1:45] The 5-Column Sales Pipeline Board
**Visual:** Demonstrate filtering by channel (WhatsApp, Facebook, Website, Phone), searching for names/phones, and changing statuses.

> "Let's start on the **Sales Pipeline Board**. 
>
> You'll notice immediately that this board only contains qualified **sales enquiries**. Notice the five distinct lifecycle stages: **New**, **Contacted**, **Interested**, **Paid**, and **Lost**.
>
> Each card gives the admissions counselor instant clarity:
> 1. The prospect's name and normalized phone number (`01XXXXXXXXX`).
> 2. Badges indicating the incoming channel and whether they want our 3-Day Bootcamp, 6-Month Fellowship, or Corporate Training.
> 3. An **Overdue Badge (48h+)** that automatically highlights leads that haven't been touched in over two days.
> 4. A clean status dropdown. When I change a card from 'New' to 'Contacted', notice how the timestamp `last_contacted_at` is updated automatically in SQLite."

---

### [1:45 - 3:00] AI Extraction & Language-Matched Replies
**Visual:** Click 'New Enquiry', paste an informal Banglish WhatsApp message, click 'Extract with AI', show the auto-filled form and the suggested reply.

> "Now, let’s see the real superpower of this CRM: **AI Message Extraction**.
>
> Imagine an admissions counselor receives this raw WhatsApp message:
> *'Assalamualaikum, apnader 3 day bootcamp er price koto? Payment kibhabe korbo?'*
>
> I paste it into the box, choose WhatsApp, and hit **'Extract with AI'**.
>
> In just a second:
> - The hybrid extractor converts any Bangla digits, runs phone regex, detects the language as **Banglish**, classifies the track as **Bootcamp**, and categorizes the enquiry as **Sales**.
> - The form is instantly pre-filled, allowing the counselor to verify or edit anything.
> - Look below: **AI Suggested Reply**. Because the sender wrote in Banglish, Gemini drafts a polite, enthusiastic reply in natural **Banglish** with exact course pricing, live class details, and next steps — ready to copy with a single click!
> - If the user writes in English, the AI replies in fluent English. If they write in Bengali script, it matches with polite Banglish as requested by the institute rules."

---

### [3:00 - 3:45] Non-Sales Isolation: Support, Job Seekers & Spam
**Visual:** Navigate to the 'Other Enquiries' tab (`/other`).

> "What happens when an incoming message isn't a sales inquiry?
>
> For example:
> - A customer complaining about a bKash payment confirmation or asking for a refund.
> - An applicant looking for an AI internship.
> - Or crypto spam.
>
> Our hybrid classifier automatically flags them as `support`, `job_seeker`, or `spam`. They are routed directly to the **Other Enquiries** view so our sales pipeline remains 100% clean and focused on revenue. Support agents can handle refunds and job inquiries right here."

---

### [3:45 - 4:30] Executive Weekly Summary & Overdue Monitoring
**Visual:** Navigate to the 'Weekly Summary' tab (`/summary`).

> "Next, let’s look at the **Executive Summary & Overdue Reports**.
>
> Here, BIAI management gets an executive snapshot powered by Gemini:
> - Total enquiry volume and channel breakdown (WhatsApp vs Facebook vs Website).
> - Program demand trends (Bootcamp vs Fellowship vs Corporate).
> - An actionable list of leads that have been waiting for over 48 hours, allowing counselors to update statuses on the spot.
> - AI-generated tactical recommendations for the week."

---

### [4:30 - 5:00] Resilience & Production Architecture
**Visual:** Show backend code / terminal passing all pytest test suites.

> "Finally, let's talk about **resilience**:
> - We built a hybrid fallback architecture. If Google Gemini experiences network latency or rate-limiting, the system never crashes. It seamlessly uses our deterministic phone regex, Bangla digit mapping, and bilingual templates.
> - The backend runs on FastAPI with SQLite and APScheduler, while the frontend is a responsive Vue 3 Single Page Application with Pinia and Vue Router.
>
> Thank you for watching, and we look forward to empowering BIAI's admissions and growth!"
