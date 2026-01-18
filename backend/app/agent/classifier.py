def classify_question(question: str) -> bool:
    """
    Return True ONLY if the question explicitly references course material.
    """
    keywords = [
        "according to",
        "knowledgebase",
        "lecture",
        "slides",
        "chapter",
        "section",
        "pdf",
        "notes",
    ]

    q = question.lower()

    return any(k in q for k in keywords)