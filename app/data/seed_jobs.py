from typing import Dict
from app.models.schemas import JobDescription

SEED_JOBS: Dict[str, JobDescription] = {
    "staff_ai_engineer": JobDescription(
        id="staff_ai_engineer",
        title="Staff AI & Systems Architect",
        seniority="Staff",
        required_skills=["Python", "FastAPI", "Docker", "LLM", "PostgreSQL", "Kubernetes", "Microservices"],
        preferred_skills=["Redis", "LangChain", "System Design", "CI/CD", "AWS"],
        min_years_experience=7.0,
        description="Lead the architecture, development, and scalability of multi-agent AI platforms and high-throughput microservices."
    ),
    "fullstack_engineer": JobDescription(
        id="fullstack_engineer",
        title="Senior Full-Stack Engineer",
        seniority="Senior",
        required_skills=["React", "TypeScript", "Python", "FastAPI", "REST API", "Docker"],
        preferred_skills=["Next.js", "Tailwind", "PostgreSQL", "GraphQL"],
        min_years_experience=5.0,
        description="Build responsive user interfaces and robust backend APIs for enterprise data-intensive AI workflows."
    )
}

