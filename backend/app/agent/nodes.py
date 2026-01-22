
from app.agent.classifier import classify_question
from app.rag.retrieve  import retrieve_context
from app.llm.client import OllamaClient
import app.agent.state as state
from app.agent.router import route_question
from app.llm.generation import generate_answer_with_context
from app.rag.citation import format_citations
import time
from app.core.logging import logger
import logging

llm = OllamaClient()

def decide_node(state: state.AgentState):
    if state.get("force_rag"):
        return {
            **state,
            "use_rag": True,
            "decision_reason": "forced by course context",
        }

    decision = route_question(state["question"])
    return {
        **state,
        "use_rag": decision["use_rag"],
        "decision_reason": decision["reason"],
}

def rag_node(state: state.AgentState):
    retrieval = retrieve_context(
        query=state["question"],
        course_code=state.get("course_code"),
    )

    chunks = retrieval["chunks"]
    confidence = retrieval["confidence"]

    # 🔒 HARD ACADEMIC GUARANTEE
    if confidence == "none":
        return {
            "answer": (
                "This question is not answered in the provided course materials."
            ),
            "source": f"rag:{state.get('course_code')}",
            "citations": [],
            "confidence": "none",
        }

    answer, citations = generate_answer_with_context(
        question=state["question"],
        context=chunks,
    )
    follow_up = None
    if confidence in ("low", "medium"):
        follow_up = "clarify_or_general"

    return {
        "answer": answer,
        "source": f"rag:{state.get('course_code')}",
        "citations": citations,
        "confidence": confidence,
        "follow_up": follow_up,
    }

def llm_node(state: state.AgentState) -> state.AgentState:
    if state.get("context"):
        prompt = f"""
You are a university science tutor.
Use the context below to answer accurately.

Context:
{state['context']}

Question:
{state['question']}

Answer:
""".strip()
    else:
        prompt = state["question"]

    start = time.time()
    answer = llm.generate(prompt)
    logger.info("LLM inference completed", extra={"latency_ms": int((time.time()-start)*1000)})

    return {
        **state,
        "answer": answer,
        "source": "llm",
    }
