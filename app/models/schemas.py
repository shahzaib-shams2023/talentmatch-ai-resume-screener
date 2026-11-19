from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class CandidateProfile(BaseModel):
    name: str
    email: Optional[str] = None
    years_experience: float
    skills: List[str]
    education: Optional[str] = None
    summary: str
    is_anonymized: bool = False


class JobDescription(BaseModel):
    id: str
    title: str
    seniority: str  # Senior, Staff, Lead, Mid
    required_skills: List[str]
    preferred_skills: List[str]
    min_years_experience: float
    description: str


class RubricScores(BaseModel):
    tech_stack_match: float = Field(..., ge=0, le=100)
    experience_depth: float = Field(..., ge=0, le=100)
    architectural_design: float = Field(..., ge=0, le=100)
    impact_and_metrics: float = Field(..., ge=0, le=100)
    education_foundation: float = Field(..., ge=0, le=100)
    overall_score: float = Field(..., ge=0, le=100)


class GapAnalysis(BaseModel):
    missing_required_skills: List[str]
    missing_preferred_skills: List[str]
    experience_gap_years: float
    strengths: List[str]
    weaknesses: List[str]


class InterviewQuestion(BaseModel):
    category: str
    question: str
    target_competency: str
    evaluation_criteria: str


class EvaluationReport(BaseModel):
    evaluation_id: str
    candidate: CandidateProfile
    job_title: str
    recommendation: str  # STRONG_YES, YES, LEANING_NO, REJECT
    rubric: RubricScores
    gap_analysis: GapAnalysis
    interview_guide: List[InterviewQuestion]
    summary_verdict: str
    evaluated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class EvaluateRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_id: Optional[str] = None
    custom_job_description: Optional[str] = None
    anonymize: bool = False

