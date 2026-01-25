from app.llm.client import OllamaClient
from typing import Optional

llm = OllamaClient()


from typing import Optional

def generate_answer_with_context(
    question: str,
    context: list[dict],
    extra_context: Optional[str] = None,
):
    if not context:
        return (
            "This question is not answered in the provided course materials.",
            [],
        )

    course_context = "\n".join(c["text"] for c in context)

    supplemental = ""
    if extra_context:
        supplemental = f"""
Supplemental material provided by the user:
{extra_context}
"""

    prompt = f"""
You are a university science tutor.

Rules:
- Answer using the official course material first.
- Use supplemental material only to clarify or expand.
- If the answer is not present in the course material, say so explicitly.
- Do NOT invent facts.

Course Material:
{course_context}

{supplemental}

Question:
{question}

Answer:
""".strip()

    answer = llm.generate(prompt)

    citations = []
    for c in context:
        meta = c.get("metadata", {})
        document = meta.get("document", "unknown")
        chunk_index = meta.get("chunk_index")

        citations.append({
            "document": document,
            "chunk": chunk_index,
            "ref": f"{document} (chunk {chunk_index})",
        })

    return answer, citations