
from app.agent.classifier import classify_question
from app.rag.retrieve  import retrieve_context
from app.llm.client import OllamaClient
import app.agent.state as state
from app.agent.router import route_question


llm = OllamaClient()

def decide_node(state: state.AgentState) -> state.AgentState:
    decision = route_question(state["question"])
    course_hint = None
    if "this course" in state["question"].lower():
        course_hint = "University Sciences"
    print(
        f"AGENT ROUTER → use_rag={decision['use_rag']} | "
        f"reason={decision['reason']}"
    )

    return {
         **state, "use_rag": decision["use_rag"], 
         "decision_reason": decision["reason"],
         "course_hint": course_hint}


def rag_node(state: state.AgentState) -> state.AgentState:
    context = retrieve_context(
        state["question"],
        course=state.get("course_hint"),
    )
    return {**state, "context": context}


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
        return {**state, "answer": answer}
