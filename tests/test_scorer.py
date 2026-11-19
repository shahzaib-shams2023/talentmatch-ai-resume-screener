import pytest
from app.evaluator.parser import ResumeParser
from app.evaluator.rubric_scorer import RubricScorer
from app.data.seed_jobs import SEED_JOBS
from app.data.seed_resumes import SEED_RESUMES


def test_rubric_scorer_staff_candidate():
    raw = SEED_RESUMES["alex_mercer_staff_architect"]
    job = SEED_JOBS["staff_ai_engineer"]
    cand = ResumeParser.parse_resume(raw)

    rubric, gaps = RubricScorer.evaluate(cand, job, raw)
    assert rubric.overall_score >= 85.0
    assert rubric.tech_stack_match >= 80.0
    assert rubric.experience_depth >= 85.0
    assert len(gaps.strengths) >= 2


def test_rubric_scorer_misaligned_candidate():
    raw = SEED_RESUMES["casey_taylor_junior_frontend"]
    job = SEED_JOBS["staff_ai_engineer"]
    cand = ResumeParser.parse_resume(raw)

    rubric, gaps = RubricScorer.evaluate(cand, job, raw)
    assert rubric.overall_score < 60.0
    assert len(gaps.missing_required_skills) > 0

