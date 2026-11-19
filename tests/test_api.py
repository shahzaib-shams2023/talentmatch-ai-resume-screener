from fastapi.testclient import TestClient
from app.main import app
from app.data.seed_resumes import SEED_RESUMES

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"


def test_get_jobs_and_resumes():
    res_jobs = client.get("/api/jobs")
    assert res_jobs.status_code == 200
    assert "staff_ai_engineer" in res_jobs.json()

    res_resumes = client.get("/api/resumes")
    assert res_resumes.status_code == 200
    assert "alex_mercer_staff_architect" in res_resumes.json()


def test_evaluate_candidate():
    payload = {
        "resume_text": SEED_RESUMES["alex_mercer_staff_architect"],
        "job_id": "staff_ai_engineer",
        "anonymize": True
    }
    res = client.post("/api/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["recommendation"] == "STRONG_YES"
    assert data["candidate"]["is_anonymized"] is True
    assert len(data["interview_guide"]) >= 3
    assert data["rubric"]["overall_score"] > 80.0

