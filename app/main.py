from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
import os

from app.config import settings
from app.models.schemas import EvaluateRequest, EvaluationReport, JobDescription
from app.evaluator.parser import ResumeParser
from app.evaluator.rubric_scorer import RubricScorer
from app.evaluator.interview_guide import InterviewGuideGenerator
from app.data.seed_jobs import SEED_JOBS
from app.data.seed_resumes import SEED_RESUMES

app = FastAPI(
    title=settings.app_name,
    description="TalentMatch AI Resume Screening & Rubric Evaluation Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    root_index = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    if os.path.exists(root_index):
        return FileResponse(root_index)
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "TalentMatch AI Resume Screening API is online."}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.environment
    }


@app.get("/api/jobs")
async def get_jobs():
    return SEED_JOBS


@app.get("/api/resumes")
async def get_resumes():
    return SEED_RESUMES


@app.post("/api/evaluate", response_model=EvaluationReport)
async def evaluate_candidate_resume(request: EvaluateRequest):
    try:
        # Determine job specification
        job = SEED_JOBS.get(request.job_id or "staff_ai_engineer")
        if not job and request.custom_job_description:
            job = JobDescription(
                id="custom_job",
                title="Custom Role",
                seniority="Senior",
                required_skills=["Python", "FastAPI", "Docker"],
                preferred_skills=["Kubernetes", "PostgreSQL"],
                min_years_experience=5.0,
                description=request.custom_job_description
            )
        elif not job:
            job = list(SEED_JOBS.values())[0]

        # Step 1: Parse & optionally anonymize resume
        candidate = ResumeParser.parse_resume(request.resume_text, anonymize=request.anonymize)

        # Step 2: Score against 5-pillar rubric & calculate gaps
        rubric, gap_analysis = RubricScorer.evaluate(candidate, job, request.resume_text)

        # Step 3: Generate targeted interview guide
        interview_guide = InterviewGuideGenerator.generate_questions(candidate, job, gap_analysis)

        # Step 4: Determine hiring recommendation
        if rubric.overall_score >= 88.0:
            recommendation = "STRONG_YES"
            verdict = f"Exceptional candidate profile exceeding requirements for {job.title}. Expedite to onsite interview."
        elif rubric.overall_score >= 70.0:
            recommendation = "YES"
            verdict = f"Strong candidate demonstrating core competencies with minor gaps. Proceed to technical screen."
        elif rubric.overall_score >= 50.0:
            recommendation = "LEANING_NO"
            verdict = f"Candidate possesses foundational skills but lacks seniority and key technologies required for {job.title}."
        else:
            recommendation = "REJECT"
            verdict = f"Significant misalignment between candidate skills and {job.title} prerequisites."

        return EvaluationReport(
            evaluation_id=f"EVAL-{str(uuid.uuid4())[:8].upper()}",
            candidate=candidate,
            job_title=job.title,
            recommendation=recommendation,
            rubric=rubric,
            gap_analysis=gap_analysis,
            interview_guide=interview_guide,
            summary_verdict=verdict
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation pipeline error: {str(e)}")

