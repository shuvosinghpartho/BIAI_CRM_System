# BIAI CRM — Admissions & Lead Pipeline Management

A full-stack, AI-powered CRM built for **BIAI (Bangladesh AI Institute)** to manage enquiries across WhatsApp, Facebook, Website, and Phone calls. Features entity extraction from informal messages (Bangla, Banglish, and English), smart language-matched reply suggestions, a 5-stage card-type sales pipeline, non-sales lead isolation, 48-hour follow-up alerts, and an executive AI weekly summary.

---

## ⚡ Instant One-Click Terminal Shortcuts

### Start All Services (Backend + Frontend + Database)
```bash
./start.sh
```
This automatically verifies dependencies, initializes the database with the 20 sample enquiries, starts the FastAPI backend daemon on port `8000`, starts the Vite frontend daemon on port `5173`, and waits until all health checks pass.

### Stop All Services
```bash
./stop.sh
```
Instantly shuts down all running backend, frontend, and database worker processes and frees ports `8000` and `5173`.

---

## 🌐 Application URLs

| Service | Local URL | Description |
|---|---|---|
| **Frontend Web App** | **[http://localhost:5173](http://localhost:5173)** | Card-type responsive dashboard with Light & Ash-Black-Red themes |
| **Sales Pipeline Board** | **[http://localhost:5173/](http://localhost:5173/)** | 5-stage Kanban board with instant status switcher |
| **New Enquiry & AI Extraction** | **[http://localhost:5173/add](http://localhost:5173/add)** | Paste messages in Bangla/Banglish/English to auto-extract fields |
| **Other Enquiries (Non-Sales)** | **[http://localhost:5173/other](http://localhost:5173/other)** | Segregated support complaints, job seeker requests, and spam |
| **Weekly AI Summary & Overdue** | **[http://localhost:5173/summary](http://localhost:5173/summary)** | Executive analytics and leads needing immediate follow-up |
| **Interactive API Docs (Swagger)**| **[http://localhost:8000/docs](http://localhost:8000/docs)** | FastAPI interactive OpenAPI documentation |
| **Backend Health Check** | **[http://localhost:8000/health](http://localhost:8000/health)** | API health status probe |

---

## 🎨 Theme System
- **Dark Theme:** Deep Pitch Black (`#09090b`), Ash Black charcoal cards (`#121215` / `#18181c`), subtle ash borders (`#27272a`), and vibrant **BIAI Crimson Red** (`#ef4444`) accents and glowing indicators.
- **Light Theme:** Ultra-clean cloud white (`#ffffff`), ice-slate column decks (`#f1f5f9`), crisp zinc borders (`#e2e8f0`), and crimson red highlights.
- Toggle between Light and Dark mode using the **Sun / Moon** switcher in the top navigation bar. Preferences persist automatically in `localStorage`.

---

## 🛠️ Tech Stack
- **Backend:** Python 3.9+, FastAPI, SQLAlchemy, SQLite, APScheduler, python-dotenv, google-genai, Pytest
- **Frontend:** Vue 3 (Composition API, `<script setup>`), Vite, Vue Router, Pinia, Axios, Modern CSS Tokens
- **Network Proxy:** Vite proxies all `/api` endpoints directly to `http://localhost:8000`.

---

## 🧪 Running Automated Tests

```bash
# 1. Database CRUD tests
PYTHONPATH=backend backend/venv/bin/pytest backend/tests/test_crud.py

# 2. Rule extraction and Bangla digit tests
PYTHONPATH=backend backend/venv/bin/pytest backend/tests/test_rules.py

# 3. Full 20-sample extraction test suite
PYTHONPATH=backend backend/venv/bin/pytest -s backend/tests/test_extract.py
```
