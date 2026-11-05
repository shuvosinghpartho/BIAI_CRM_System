import csv
import sys
from pathlib import Path
import pytest

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.language import detect_language, get_reply_language
from app.services.rules import (
    convert_bangla_digits,
    extract_phone,
    extract_interest,
    extract_enquiry_type,
    extract_name_from_text,
    extract_with_rules,
)

def test_convert_bangla_digits():
    assert convert_bangla_digits("০১২৩৪৫৬৭৮৯") == "0123456789"
    assert convert_bangla_digits("ফোন: ০১৭১১-০০০০০১") == "ফোন: 01711-000001"

def test_extract_phone_formats():
    assert extract_phone("My number is 01711000001") == "01711000001"
    assert extract_phone("Call me on +8801711000003 today") == "01711000003"
    assert extract_phone("যোগাযোগ: ০১৭১১০০০০০৭") == "01711000007"
    assert extract_phone("No phone number here") is None

def test_language_detection():
    # Bangla script
    assert detect_language("ফেলোশিপ প্রোগ্রামে ভর্তি হতে চাই।") == "bangla"
    assert detect_language("আমার কোম্পানির ১৫ জন কর্মীর জন্য") == "bangla"

    # Banglish (Latin script with Bengali words)
    assert detect_language("Assalamualaikum, apnader 3 day bootcamp er price koto?") == "banglish"
    assert detect_language("Ei course korle job pabo?") == "banglish"
    assert detect_language("Offline class kothay hobe?") == "banglish"

    # English
    assert detect_language("I run a 40-person textile company in Gazipur.") == "english"
    assert detect_language("Do you offer refunds if I cannot attend after paying?") == "english"
    assert detect_language("Looking for a job as an AI intern. Where do I apply?") == "english"

def test_reply_language_mapping():
    assert get_reply_language("english") == "english"
    assert get_reply_language("bangla") == "bangla"
    assert get_reply_language("banglish") == "banglish"

def test_all_20_samples_rules():
    csv_path = Path(__file__).resolve().parent.parent.parent / "data" / "sample-enquiries.csv"
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 20

    results = []
    for row in reader:
        msg = row["message"]
        lang = detect_language(msg)
        phone = extract_phone(row["phone"] or msg)
        interest = extract_interest(msg)
        etype = extract_enquiry_type(msg)
        results.append({
            "id": row["id"],
            "lang": lang,
            "phone": phone,
            "interest": interest,
            "etype": etype,
        })

    # Spot checks on specific IDs
    # ID 1: Banglish, bootcamp, sales
    assert results[0]["lang"] == "banglish"
    assert results[0]["interest"] == "bootcamp"
    assert results[0]["etype"] == "sales"

    # ID 2: Bangla, fellowship, sales
    assert results[1]["lang"] == "bangla"
    assert results[1]["interest"] == "fellowship"
    assert results[1]["etype"] == "sales"

    # ID 3: English, corporate, sales
    assert results[2]["lang"] == "english"
    assert results[2]["interest"] == "corporate"
    assert results[2]["etype"] == "sales"

    # ID 7: Support (payment confirmation)
    assert results[6]["etype"] == "support"
    assert results[6]["lang"] == "bangla"

    # ID 11: Spam (crypto signals)
    assert results[10]["etype"] == "spam"

    # ID 16: Support (cancellation complaint)
    assert results[15]["etype"] == "support"

    # ID 18: Corporate (group discount for 15 employees)
    assert results[17]["interest"] == "corporate"

    # ID 20: Job seeker
    assert results[19]["etype"] == "job_seeker"

