from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import decide_node, rag_node, llm_node


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("decide", decide_node)
    graph.add_node("rag", rag_node)
    graph.add_node("llm", llm_node)

    # Entry
    graph.set_entry_point("decide")

    # Deterministic routing
    graph.add_conditional_edges(
        "decide",
        lambda state: (
            "rag" if state.course_code else
            "rag" if state.use_rag else
            "llm"
        ),
        {
            "rag": "rag",
            "llm": "llm",
        }
    )

    graph.set_finish_point("rag")
    graph.set_finish_point("llm")

    return graph.compile()


def route(state: AgentState):
    if state.course_code:
        return "rag_only"
    return "auto"
