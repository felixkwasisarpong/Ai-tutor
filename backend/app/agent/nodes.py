
from app.agent.classifier import classify_question
from app.rag.retrieve  import retrieve_context
from app.llm.client import OllamaClient
import app.agent.state as state
from app.agent.router import route_question
from app.llm.generation import generate_answer_with_context
from app.rag.citation import format_citations

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
        state["question"],
        course_code=state.get("course_code"),
    )

    results = retrieval["chunks"]
    confidence = retrieval["confidence"]

    if not results:
        return {
            "answer": "This question is not answered in the provided course materials.",
            "source": f"rag:{state.get('course_code')}",
            "citations": [],
            "confidence": "none",
        }

    # Normal RAG path
    answer, citations = generate_answer_with_context(
        question=state["question"],
        context=results,
    )

    if not citations:
        raise RuntimeError(
            "Invariant violation: RAG node produced answer without citations"
        )

    return {
        "answer": answer,
        "source": f"rag:{state.get('course_code')}",
        "citations": citations,
        "confidence": confidence,
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

    answer = llm.generate(prompt)

    return {
        **state,
        "answer": answer,
        "source": "llm",
    }
