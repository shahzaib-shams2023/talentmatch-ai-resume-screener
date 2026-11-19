import re
from typing import Tuple, List
from app.models.schemas import CandidateProfile, JobDescription, RubricScores, GapAnalysis


class RubricScorer:
    @classmethod
    def evaluate(cls, candidate: CandidateProfile, job: JobDescription, raw_text: str) -> Tuple[RubricScores, GapAnalysis]:
        cand_skills = set(s.lower() for s in candidate.skills)
        req_skills = set(s.lower() for s in job.required_skills)
        pref_skills = set(s.lower() for s in job.preferred_skills)

        # 1. Tech Stack Match
        req_overlap = len(cand_skills.intersection(req_skills))
        pref_overlap = len(cand_skills.intersection(pref_skills))
        req_pct = (req_overlap / max(len(req_skills), 1)) * 100
        pref_pct = (pref_overlap / max(len(pref_skills), 1)) * 100
        tech_score = round(min((req_pct * 0.75) + (pref_pct * 0.25), 100.0), 1)

        # 2. Experience Depth
        exp_ratio = candidate.years_experience / max(job.min_years_experience, 1.0)
        exp_score = round(min(exp_ratio * 90.0, 100.0), 1)
        if candidate.years_experience >= job.min_years_experience:
            exp_score = max(exp_score, 85.0)

        # 3. Architectural Design
        arch_keywords = ["system design", "distributed", "microservices", "scalable", "sharding", "concurrency", "event-driven", "latency"]
        text_lower = raw_text.lower()
        arch_count = sum(1 for k in arch_keywords if k in text_lower)
        arch_score = round(min(60.0 + (arch_count * 8.0), 98.0), 1)

        # 4. Impact & Metrics (presence of %, $, numbers)
        metric_matches = re.findall(r"(?:\d+%\s*(?:reduction|increase|improvement|faster|savings)|\$[\d,]+|\b\d+x\b|\b\d+\s*ms\b)", raw_text, re.IGNORECASE)
        impact_score = round(min(65.0 + (len(metric_matches) * 7.0), 96.0), 1)

        # 5. Education
        edu_score = 85.0
        if "ph.d" in (candidate.education or "").lower():
            edu_score = 98.0
        elif "m.s." in (candidate.education or "").lower():
            edu_score = 92.0

        # Weighted Overall Score
        overall = round(
            (0.30 * tech_score) +
            (0.25 * exp_score) +
            (0.20 * arch_score) +
            (0.15 * impact_score) +
            (0.10 * edu_score),
            1
        )

        rubric = RubricScores(
            tech_stack_match=tech_score,
            experience_depth=exp_score,
            architectural_design=arch_score,
            impact_and_metrics=impact_score,
            education_foundation=edu_score,
            overall_score=overall
        )

        # Gap Analysis
        missing_req = [s for s in job.required_skills if s.lower() not in cand_skills]
        missing_pref = [s for s in job.preferred_skills if s.lower() not in cand_skills]
        exp_gap = max(round(job.min_years_experience - candidate.years_experience, 1), 0.0)

        strengths = []
        if tech_score >= 80:
            strengths.append(f"Strong alignment on primary technologies: {', '.join(list(cand_skills.intersection(req_skills))[:3])}")
        if candidate.years_experience >= job.min_years_experience:
            strengths.append(f"Meets seniority requirements ({int(candidate.years_experience)} years vs {int(job.min_years_experience)} required)")
        if len(metric_matches) >= 2:
            strengths.append(f"Demonstrates business impact with quantified engineering metrics")

        weaknesses = []
        if missing_req:
            weaknesses.append(f"Missing core required competencies: {', '.join(missing_req)}")
        if exp_gap > 0:
            weaknesses.append(f"Experience deficit: {exp_gap} years below role minimum")
        if arch_count < 2:
            weaknesses.append("Limited documented system design / large-scale architecture experience")

        gap_analysis = GapAnalysis(
            missing_required_skills=missing_req,
            missing_preferred_skills=missing_pref,
            experience_gap_years=exp_gap,
            strengths=strengths or ["General software engineering foundations"],
            weaknesses=weaknesses or ["No major red flags identified"]
        )

        return rubric, gap_analysis

