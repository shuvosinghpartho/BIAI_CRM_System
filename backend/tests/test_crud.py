import sys
from pathlib import Path
from datetime import datetime
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Enquiry

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}

def test_list_enquiries():
    res = client.get("/api/enquiries")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 20

def test_create_and_patch_and_delete():
    # 1. Create
    payload = {
        "name": "Test User",
        "phone": "01700000999",
        "source": "whatsapp",
        "interest": "bootcamp",
        "status": "New",
        "enquiry_type": "sales",
        "language": "banglish",
        "message": "Test message for crud"
    }
    create_res = client.post("/api/enquiries", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    enquiry_id = created["id"]
    assert created["name"] == "Test User"
    assert created["last_contacted_at"] is None

    # 2. Get single
    get_res = client.get(f"/api/enquiries/{enquiry_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Test User"

    # 3. Patch status -> should set last_contacted_at automatically
    patch_res = client.patch(f"/api/enquiries/{enquiry_id}", json={"status": "Contacted"})
    assert patch_res.status_code == 200
    patched = patch_res.json()
    assert patched["status"] == "Contacted"
    assert patched["last_contacted_at"] is not None

    # 4. Filter by status
    filter_res = client.get("/api/enquiries?status=Contacted")
    assert filter_res.status_code == 200
    contacted_ids = [item["id"] for item in filter_res.json()]
    assert enquiry_id in contacted_ids

    # 5. Delete
    delete_res = client.delete(f"/api/enquiries/{enquiry_id}")
    assert delete_res.status_code == 204

    # 6. Verify deleted
    not_found = client.get(f"/api/enquiries/{enquiry_id}")
    assert not_found.status_code == 404

