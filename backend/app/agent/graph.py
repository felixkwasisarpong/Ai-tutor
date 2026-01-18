from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import decide_node, rag_node, llm_node


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("decide", decide_node)
    graph.add_node("rag", rag_node)
    graph.add_node("llm", llm_node)

    graph.set_entry_point("decide")
    graph.add_conditional_edges(
        "decide",
        lambda state: "rag" if state["use_rag"] else "llm",
    {
        "rag": "rag",
        "llm": "llm"
    },
    )

    graph.add_edge("rag", "llm")    
    graph.add_edge("llm", END)  # End node

    return graph.compile()
