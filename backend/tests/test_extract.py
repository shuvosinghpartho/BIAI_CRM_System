import csv
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import app
from app.services.extractor import extract_enquiry_data
from app.services.reply_service import suggest_reply
from scripts.import_csv import normalize_source

client = TestClient(app)

def test_api_extract_endpoint():
    res = client.post("/api/ai/extract", json={
        "message": "ফেলোশিপ প্রোগ্রামে ভর্তি হতে চাই। কবে শুরু হবে?",
        "source": "facebook"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["source"] == "facebook"
    assert data["interest"] == "fellowship"
    assert data["enquiry_type"] == "sales"
    assert data["language"] == "bangla"

def test_api_suggest_reply_endpoint():
    res = client.post("/api/ai/suggest-reply", json={
        "message": "Assalamualaikum, apnader 3 day bootcamp er price koto? Payment kibhabe korbo?",
        "name": "Rafi Ahmed",
        "interest": "bootcamp",
        "enquiry_type": "sales",
        "language": "banglish"
    })
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert len(data["reply"]) > 10

def test_extract_all_20_samples():
    csv_path = Path(__file__).resolve().parent.parent.parent / "data" / "sample-enquiries.csv"
    with open(csv_path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 20

    print("\n" + "=" * 125)
    print(f"{'ID':<3} | {'Type':<10} | {'Interest':<11} | {'Phone':<12} | {'Lang':<8} | Message Preview")
    print("=" * 125)

    extracted_records = []
    for r in rows:
        channel_source = normalize_source(r["channel"])
        res = extract_enquiry_data(r["message"], source=channel_source)
        
        # Phone: from message or sender if present
        phone = res.get("phone") or (r["phone"].strip() if r["phone"] else None)

        extracted_records.append({
            "id": r["id"],
            "name": res.get("name") or r["sender name"].strip() or "N/A",
            "phone": phone or "N/A",
            "source": res.get("source"),
            "interest": res.get("interest"),
            "enquiry_type": res.get("enquiry_type"),
            "language": res.get("language"),
            "message": r["message"]
        })

        msg_preview = r["message"].replace("\n", " ")[:50] + ("..." if len(r["message"]) > 50 else "")
        print(f"{r['id']:<3} | {res['enquiry_type']:<10} | {res['interest']:<11} | {str(phone or 'N/A'):<12} | {res['language']:<8} | {msg_preview}")

    print("=" * 125 + "\n")

    # Assertions on all 20 extractions
    for item in extracted_records:
        assert item["enquiry_type"] in ["sales", "support", "spam", "job_seeker"]
        assert item["interest"] in ["bootcamp", "fellowship", "corporate", "unknown"]
        assert item["language"] in ["bangla", "banglish", "english"]
