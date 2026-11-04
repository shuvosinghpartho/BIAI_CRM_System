import os
from pathlib import Path
from dotenv import load_dotenv

# Try loading .env from current directory or parent directories
env_paths = [
    Path(__file__).resolve().parent.parent / ".env",
    Path(__file__).resolve().parent.parent.parent / ".env",
    Path(".env")
]

for p in env_paths:
    if p.exists():
        load_dotenv(p)
        break

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# gemini-3.5-flash-lite delivers high quota (1,500 req/day) and low latency (~0.8s)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
FOLLOWUP_HOURS = int(os.getenv("FOLLOWUP_HOURS", "48"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm.db")
