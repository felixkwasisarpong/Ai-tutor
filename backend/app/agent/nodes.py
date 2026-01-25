
from app.agent.classifier import classify_question
from app.rag.retrieve  import retrieve_context
from app.llm.client import OllamaClient
from app.agent.state import AgentState, VerifiedContext
from app.agent.router import route_question
from app.llm.generation import generate_answer_with_context
from app.rag.citation import format_citations
import time
from app.agent.policies.homework import is_homework_question

from app.core.logging import logger

llm = OllamaClient()
CONTEXT_TTL_SECONDS = 300  # 5 minutes


def decide_node(state: AgentState):
    state_data = state.model_dump()

        #Academic integrity check
    if is_homework_question(state.question):
        return {
            **state_data,
            "use_rag": True,
            "blocked": True,
            "decision_reason": "homework question detected",
        }
    # 🔒 Rule 1: Explicit course force (unchanged)
    if state.force_rag:
        return {
            **state_data,
            "use_rag": True,
            "decision_reason": "forced by course context",
        }

    # 🧠 Rule 2: Verified academic follow-up
    verified = state.verified_context
    if verified:
        is_valid = (
            verified.course_code == state.course_code
            and verified.expires_at > time.time()
        )

        if is_valid:
            return {
                **state_data,
                "use_rag": True,
                "decision_reason": "verified academic follow-up",
            }

    # 🤖 Rule 3: Default LLM routing
    decision = route_question(state.question)
    return {
        **state_data,
        "use_rag": decision["use_rag"],
        "decision_reason": decision["reason"],
    }

def rag_node(state: AgentState):
    state_data = state.model_dump()
    retrieval = retrieve_context(
        query=state.question,
        course_code=state.course_code,
    )

    chunks = retrieval["chunks"]
    confidence = retrieval["confidence"]

    if state.blocked:
        return {
            "answer": (
                "I can’t help solve graded assignments or exams. "
                "However, I can explain the underlying concepts or walk "
                "through similar ungraded examples if you’d like."
            ),
            "source": "policy",
            "citations": [],
            "confidence": "none",
            "follow_up": "conceptual_help",
        }

    # 🔒 HARD ACADEMIC GUARANTEE (unchanged)
    if confidence == "none":
        return {
            **state_data,
            "answer": (
                "This question is not answered in the provided course materials."
            ),
            "source": f"rag:{state.course_code}",
            "citations": [],
            "confidence": "none",
            "verified_context": None,
        }

    answer, citations = generate_answer_with_context(
        question=state.question,
        context=chunks,
    )

    # 🧠 NEW: Verified academic memory (ONLY if citations exist)
    verified_context = None
    if citations and state.course_code:
        verified_context = VerifiedContext(
            course_code=state.course_code,
            chunks=chunks,
            expires_at=time.time() + CONTEXT_TTL_SECONDS,
        )

    follow_up = None
    if confidence in ("low", "medium"):
        follow_up = "clarify_or_general"

    return {
        **state_data,
        "answer": answer,
        "source": f"rag:{state.course_code}",
        "citations": citations,
        "confidence": confidence,
        "follow_up": follow_up,
        "verified_context": verified_context,
    }

def llm_node(state: AgentState) -> AgentState:
    state_data = state.model_dump()
    if state.context:
        prompt = f"""
You are a university science tutor.
Use the context below to answer accurately.

Context:
{state.context}

Question:
{state.question}

Answer:
""".strip()
    else:
        prompt = state.question

    start = time.time()
    answer = llm.generate(prompt)
    logger.info("LLM inference completed", extra={"latency_ms": int((time.time()-start)*1000)})

    return {
        **state_data,
        "answer": answer,
        "source": "llm",
    }
