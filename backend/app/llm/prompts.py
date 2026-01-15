def default_prompt(question: str) -> str:
    return f"""You are a university-level science tutor.
Explain clearly and accurately.

Question:
{question}

Answer:
""".strip()