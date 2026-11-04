import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import engine, Base, SessionLocal
from app.routes.enquiries import router as enquiries_router
from app.routes.ai import router as ai_router
from app.routes.reports import router as reports_router
from app.services.reminder_service import get_overdue_enquiries

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("biai_crm")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Periodic follow-up check function
def periodic_overdue_check():
    db = SessionLocal()
    try:
        overdue = get_overdue_enquiries(db)
        if overdue:
            logger.info(f"[Scheduler] Found {len(overdue)} overdue enquiries needing follow-up.")
    except Exception as e:
        logger.error(f"[Scheduler] Error running overdue check: {e}")
    finally:
        db.close()

# APScheduler configuration
scheduler = BackgroundScheduler()
scheduler.add_job(periodic_overdue_check, "interval", hours=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start scheduler
    logger.info("Starting background scheduler...")
    scheduler.start()
    yield
    # Shutdown: Stop scheduler
    logger.info("Shutting down background scheduler...")
    scheduler.shutdown(wait=False)

app = FastAPI(title="BIAI CRM API", version="1.0.0", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(enquiries_router)
app.include_router(ai_router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {"status": "ok", "app": "BIAI CRM API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
