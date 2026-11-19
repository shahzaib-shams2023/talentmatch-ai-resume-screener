from typing import List
from app.models.schemas import CandidateProfile, JobDescription, GapAnalysis, InterviewQuestion


class InterviewGuideGenerator:
    @classmethod
    def generate_questions(
        cls,
        candidate: CandidateProfile,
        job: JobDescription,
        gaps: GapAnalysis
    ) -> List[InterviewQuestion]:
        questions: List[InterviewQuestion] = []

        # 1. Gap-specific Technical Invalidation Question
        if gaps.missing_required_skills:
            missing_skill = gaps.missing_required_skills[0]
            questions.append(InterviewQuestion(
                category="Technical Gap Exploration",
                question=(
                    f"Our platform relies heavily on {missing_skill}. How have you approached learning or adopting "
                    f"analogous frameworks or patterns, and how would you ramp up within the first 30 days?"
                ),
                target_competency=f"{missing_skill} Adaptability",
                evaluation_criteria="Candidate articulates conceptual analogies, documentation review strategy, and hands-on POC methodology."
            ))
        else:
            questions.append(InterviewQuestion(
                category="Deep Technical Domain",
                question="Can you walk us through the most complex asynchronous concurrency or data pipeline challenge you have resolved in production?",
                target_competency="Advanced Systems Engineering",
                evaluation_criteria="Clear diagnosis of root cause (race conditions, memory leaks, I/O bottlenecks) and verified benchmarking."
            ))

        # 2. System Design & Architectural Scalability
        questions.append(InterviewQuestion(
            category="System Design & Tradeoffs",
            question=(
                f"For our {job.title} scope: How would you design a high-throughput, low-latency ingestion service handling "
                "10,000 requests/sec with strict data durability guarantees?"
            ),
            target_competency="Distributed Systems Architecture",
            evaluation_criteria="Addresses partitioned queuing (Kafka/SQS), idempotency, connection pooling, and circuit breaker patterns."
        ))

        # 3. Ownership & Quantified Engineering Impact
        questions.append(InterviewQuestion(
            category="Measurable Business Impact",
            question="Describe an engineering project where you had to push back on requirements or technical debt to deliver measurable business performance.",
            target_competency="Technical Leadership & Pragmatism",
            evaluation_criteria="Demonstrates balance between engineering purity and product shipment velocity with concrete metrics."
        ))

        # 4. Collaborative Conflict & Code Quality
        questions.append(InterviewQuestion(
            category="Team Collaboration & Mentorship",
            question="Tell me about a disagreement you had with a senior teammate during an architectural RFC or PR review. How was consensus reached?",
            target_competency="Constructive Disagreement & Empathy",
            evaluation_criteria="Shows maturity, focus on objective data/benchmarks rather than ego, and commitment to shared standards."
        ))

        return questions

