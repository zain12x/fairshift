from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_landing():
    res = client.get("/")
    assert res.status_code == 200
    assert "FairShift" in res.text

def test_worker_portal():
    res = client.get("/worker")
    assert res.status_code == 200
    assert "Worker Portal" in res.text

def test_hazard_report():
    res = client.post("/report-hazard", data={"sector": "Construction", "desc": "Wobbly ladder on site"})
    assert res.status_code == 200

def test_admin_portal():
    res = client.get("/admin")
    assert res.status_code == 200
    assert "Workforce Health Dashboard" in res.text
