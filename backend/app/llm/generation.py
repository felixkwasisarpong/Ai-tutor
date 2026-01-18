from app.llm.client import OllamaClient

llm = OllamaClient()


def generate_answer_with_context(
    question: str,
    context: list[str],
) -> str:
    """
    Generate an answer grounded strictly in retrieved course context.
    """

    if not context:
        return (
            "I could not find relevant information in the course materials "
            "to answer this question."
        )

    context_block = "\n\n".join(
        f"- {chunk}" for chunk in context
    )

    prompt = f"""
You are an academic tutor.

Answer the question using ONLY the provided course materials.
If the answer is not present in the materials, say you do not know.

Course Materials:
{context_block}

Question:
{question}

Answer:
""".strip()

    return llm.generate(prompt)