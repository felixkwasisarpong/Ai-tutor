from app.llm.client import OllamaClient

llm = OllamaClient()


def generate_answer_with_context(question: str, context: list[dict]):
    if not context:
        return (
            "I could not find relevant information in the course materials.",
            [],
        )

    context_block = "\n\n".join(
        f"[{i}] {c['text']}" for i, c in enumerate(context)
    )

    prompt = f"""
You are an academic tutor.
Answer using ONLY the numbered course excerpts below.
If the answer is not present, say so.

Course Materials:
{context_block}

Question:
{question}

Answer:
""".strip()

    answer = llm.generate(prompt)

    citations = [
        {
            "document": c["metadata"].get("document"),
            "chunk": c["metadata"].get("chunk_index"),
        }
        for c in context
    ]

    return answer, citations

