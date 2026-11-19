import pytest
from app.evaluator.parser import ResumeParser
from app.data.seed_resumes import SEED_RESUMES


def test_parse_candidate_profile():
    raw = SEED_RESUMES["alex_mercer_staff_architect"]
    profile = ResumeParser.parse_resume(raw, anonymize=False)
    assert profile.name == "Alex Mercer"
    assert profile.email == "alex.mercer@ai-engineering.dev"
    assert profile.years_experience >= 10.0
    assert "Python" in profile.skills
    assert "Fastapi" in profile.skills
    assert "Docker" in profile.skills
    assert profile.is_anonymized is False


def test_anonymize_candidate_profile():
    raw = SEED_RESUMES["alex_mercer_staff_architect"]
    profile = ResumeParser.parse_resume(raw, anonymize=True)
    assert "Alex Mercer" not in profile.name
    assert "Candidate #" in profile.name
    assert "anonymized" in profile.email
    assert profile.is_anonymized is True

