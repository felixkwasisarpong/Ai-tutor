from typing import List, Optional


def format_citations(citations: List[dict]) -> List[dict]:
    """
    Format citations from agent state to API response format.
    """
    formatted = []
    for c in citations:
        document = c.get("document", "Unknown document")
        chunk = c.get("chunk")
        if chunk is not None:
            ref = f"{document} (chunk {chunk})"
        else:
            ref = document
        formatted.append(
            {
            **c,"ref":ref
            }
        )

    return formatted
                          