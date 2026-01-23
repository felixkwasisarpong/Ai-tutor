from app.llm.client import OllamaClient
from app.core.logging import logger
llm = OllamaClient()


def generate_answer_with_context(question: str, context: list[dict]):
    if not context:
        return (
            "This question is not answered in the provided course materials.",
            [],
        )

    prompt = f"""
You are a university science tutor.
Answer ONLY using the context below.
If the answer is not present, say so explicitly.

Context:
{chr(10).join(c["text"] for c in context)}

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