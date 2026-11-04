import csv
import sys
from datetime import datetime
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import engine, Base, SessionLocal
from app.models import Enquiry
from app.services.extractor import extract_enquiry_data
from app.services.rules import extract_with_rules

def normalize_source(channel: str) -> str:
    c = channel.strip().lower()
    if "whatsapp" in c:
        return "whatsapp"
    if "facebook" in c:
        return "facebook"
    if "website" in c:
        return "website"
    if "phone" in c:
        return "phone"
    return "website"

def import_csv():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    csv_paths = [
        Path(__file__).resolve().parent.parent.parent / "data" / "sample-enquiries.csv",
        Path("data/sample-enquiries.csv"),
        Path("../data/sample-enquiries.csv"),
    ]
    
    csv_file = None
    for p in csv_paths:
        if p.exists():
            csv_file = p
            break

    if not csv_file:
        print(f"Error: Could not find sample-enquiries.csv in {[str(p) for p in csv_paths]}")
        sys.exit(1)

    print(f"Reading sample enquiries from {csv_file}...")

    # Clear existing rows to prevent duplicate runs
    db.query(Enquiry).delete()
    db.commit()

    imported_count = 0
    with open(csv_file, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            enquiry_id = int(row["id"].strip())
            channel = row["channel"].strip()
            source = normalize_source(channel)
            received_str = row["received at"].strip()
            created_at = datetime.strptime(received_str, "%Y-%m-%d %H:%M")
            sender_name = row["sender name"].strip() or None
            phone = row["phone"].strip() or None
            message = row["message"].strip()

            # Fast rule-based classification during batch import to ensure immediate readiness
            extracted = extract_with_rules(message, default_source=source)

            enquiry = Enquiry(
                id=enquiry_id,
                name=sender_name or extracted.get("name"),
                phone=phone or extracted.get("phone"),
                source=source,
                interest=extracted.get("interest", "unknown"),
                status="New",
                enquiry_type=extracted.get("enquiry_type", "sales"),
                language=extracted.get("language", "english"),
                message=message,
                ai_reply=None,
                created_at=created_at,
                last_contacted_at=None,
            )
            db.add(enquiry)
            imported_count += 1

    db.commit()
    print(f"Successfully imported {imported_count} enquiries with enriched classification.\n")

    # Fetch and display the 20 imported rows from SQLite
    rows = db.query(Enquiry).order_by(Enquiry.id).all()
    print("=" * 115)
    print(f"{'ID':<4} | {'Name':<22} | {'Phone':<13} | {'Source':<10} | {'Interest':<11} | {'Type':<10} | {'Lang':<8}")
    print("=" * 115)
    for r in rows:
        name_str = (r.name or "N/A")[:22]
        phone_str = (r.phone or "N/A")[:13]
        print(f"{r.id:<4} | {name_str:<22} | {phone_str:<13} | {r.source:<10} | {r.interest:<11} | {r.enquiry_type:<10} | {r.language or 'N/A':<8}")
    print("=" * 115)

    db.close()

if __name__ == "__main__":
    import_csv()
