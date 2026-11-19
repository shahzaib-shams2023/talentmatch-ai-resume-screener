import re
from typing import List, Tuple
from app.models.schemas import CandidateProfile

COMMON_TECH_SKILLS = [
    "python", "fastapi", "react", "next.js", "typescript", "javascript",
    "docker", "kubernetes", "aws", "gcp", "azure", "postgresql", "sqlite",
    "redis", "graphql", "rest api", "llm", "langchain", "pytorch",
    "ci/cd", "microservices", "sql", "git", "linux", "system design"
]


class ResumeParser:
    @classmethod
    def parse_resume(cls, text: str, anonymize: bool = False) -> CandidateProfile:
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # 1. Name & Email extraction
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", text)
        email = email_match.group(0) if email_match else None

        # Candidate name usually on first line
        raw_name = lines[0] if lines else "Candidate"
        if len(raw_name) > 40 or "@" in raw_name:
            raw_name = "Candidate"

        # 2. Years of Experience
        exp_matches = re.findall(r"(\d+)\+?\s*years?(?:\s+of)?\s+experience", text, re.IGNORECASE)
        if exp_matches:
            years = float(exp_matches[0])
        else:
            # Estimate by counting job date intervals
            date_matches = re.findall(r"\b(?:20\d{2}|19\d{2})\b", text)
            if len(date_matches) >= 2:
                years = max(float(max(map(int, date_matches)) - min(map(int, date_matches))), 1.0)
            else:
                years = 5.0

        # 3. Skills extraction
        text_lower = text.lower()
        extracted_skills = []
        for skill in COMMON_TECH_SKILLS:
            if re.search(rf"\b{re.escape(skill)}\b", text_lower):
                extracted_skills.append(skill.title())

        # 4. Education
        edu = "B.S. in Computer Science"
        if "phd" in text_lower or "ph.d" in text_lower:
            edu = "Ph.D. in Computer Science / AI"
        elif "master" in text_lower or "m.s." in text_lower:
            edu = "M.S. in Computer Science"
        elif "bachelor" in text_lower or "b.s." in text_lower:
            edu = "B.S. in Computer Science"

        summary = lines[1] if len(lines) > 1 else "Experienced Software Engineer."

        # Apply bias anonymization
        if anonymize:
            cand_id = abs(hash(text)) % 9000 + 1000
            name = f"Candidate #{cand_id} (Anonymized Profile)"
            email = f"candidate-{cand_id}@anonymized.talent.local"
        else:
            name = raw_name

        return CandidateProfile(
            name=name,
            email=email,
            years_experience=years,
            skills=extracted_skills,
            education=edu,
            summary=summary,
            is_anonymized=anonymize
        )

