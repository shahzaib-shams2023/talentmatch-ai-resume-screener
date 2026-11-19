# TalentMatch AI: Resume Screening & Rubric Evaluation Platform

TalentMatch AI is an intelligent recruiting platform designed to parse candidate resumes, evaluate competency fit across multi-dimensional rubric dimensions, mitigate unconscious hiring bias, and generate tailored technical interview guides.

---

## 🔍 The Problem
Technical recruiting is overwhelmed by massive applicant volumes. Legacy screening workflows suffer from two opposite extremes:
1. **Brittle Keyword Filters**: Reject qualified non-traditional candidates due to minor wording variations while rewarding resume keyword-stuffing.
2. **Unconscious Bias & Subjectivity**: Unstandardized reviews introduce bias based on demographic indicators, alma maters, or personal preferences, leading to inequitable hiring decisions.

## 💡 The Solution
TalentMatch AI replaces arbitrary keyword counts with structured, rubric-based evaluation:
1. **Resume Parser**: Extracts structured profiles (experience tenure, technical competencies, education, and quantified business impact metrics).
2. **5-Pillar Rubric Scoring**:
   - **Tech Stack Alignment**: Measures required and preferred skill overlap.
   - **Experience Depth**: Evaluates seniority against role requirements.
   - **Architectural & System Design**: Identifies evidence of distributed systems, scaling, and fault tolerance.
   - **Impact & Metrics**: Rewards quantified engineering deliverables (latency reductions, cost savings, throughput).
   - **Educational Foundation**: Recognizes relevant degrees and credentials.
3. **Unconscious Bias Mitigation**: Provides a one-click blind review mode that redacts candidate names, emails, and demographic identifiers before scoring.
4. **Tailored Interview Guides**: Generates specific technical and behavioral questions targeted directly at candidate qualification gaps.

---

## 🏛️ System Architecture

```
Candidate Resume (Text, Markdown) + Job Description
                      │
                      ▼
     [Resume Parser & Anonymization Engine]
                      │
                      ▼
        [5-Pillar Rubric Evaluator]
         - Tech Stack Alignment
         - Experience Depth
         - Architectural Design
         - Measurable Impact
         - Education Foundation
                      │
                      ▼
     ┌────────────────┴────────────────┐
     ▼                                 ▼
[Gap Analysis]          [Tailored Interview Guide]
     │                                 │
     └────────────────┬────────────────┘
                      ▼
    Scorecard, Radar Chart & REST API
```

---

## 🛠️ Technology Stack
- **Backend**: Python 3.11, FastAPI, Pydantic v2
- **Evaluation**: Weighted Rubric Engine, Regex Heuristics
- **Frontend**: Responsive Recruiter Studio (Tailwind CSS, Chart.js Radar)
- **Testing**: Pytest, Starlette TestClient
- **Deployment**: Docker, Docker Compose, GitHub Actions CI

---

## 🚀 Getting Started

### Installation
```bash
cd talentmatch-ai-resume-screener

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### Running the Application
```bash
python -m uvicorn app.main:app --reload --port 8004
```
Access the Recruiter Studio at `http://localhost:8004` or inspect OpenAPI docs at `http://localhost:8004/docs`.

---

## 🧪 Running Automated Tests
```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment
```bash
docker compose up --build
```
Access the application at `http://localhost:8004`.

---

## 📡 API Reference

### Evaluate Resume
`POST /api/evaluate`
```json
{
  "resume_text": "Alex Mercer\nStaff Software Architect with 10+ years...",
  "job_id": "staff_ai_engineer",
  "anonymize": true
}
```

Response:
```json
{
  "evaluation_id": "EVAL-A1B2C3D4",
  "candidate": {
    "name": "Candidate #7192 (Anonymized Profile)",
    "years_experience": 10.0,
    "is_anonymized": true
  },
  "job_title": "Staff AI & Systems Architect",
  "recommendation": "STRONG_YES",
  "rubric": {
    "tech_stack_match": 88.5,
    "experience_depth": 100.0,
    "architectural_design": 92.0,
    "impact_and_metrics": 86.0,
    "education_foundation": 92.0,
    "overall_score": 91.2
  },
  "gap_analysis": {
    "missing_required_skills": [],
    "strengths": ["Strong alignment on primary technologies: Python, Fastapi, Docker"]
  },
  "interview_guide": [
    {
      "category": "Deep Technical Domain",
      "question": "Can you walk us through the most complex asynchronous concurrency...",
      "target_competency": "Advanced Systems Engineering"
    }
  ]
}
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

