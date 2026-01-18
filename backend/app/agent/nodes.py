
from app.agent.classifier import classify_question
from app.rag.retrieve  import retrieve_context
from app.llm.client import OllamaClient
import app.agent.state as state


llm = OllamaClient()

def decide_node(state: state.AgentState) -> state.AgentState:
    use_rag = classify_question(state["question"])
    print(f"AGENT DECISION -> use_rag: {use_rag}")
    return {**state,"use_rag": use_rag}


def rag_node(state: state.AgentState) -> state.AgentState:
    context = retrieve_context(state["question"])
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
