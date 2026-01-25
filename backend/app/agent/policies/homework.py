import re

HOMEWORK_PATTERNS = [
    r"\bhomework\b",
    r"\bassignment\b",
    r"\bexam\b",
    r"\bmidterm\b",
    r"\bfinal\b",
    r"\bproblem\s*\d+",
    r"\bquestion\s*\d+",
    r"\bsolve\b",
    r"\bderive\b",
    r"\bcalculate\b",
    r"\bprove\b",
    r"\bshow\s+that\b",
]

def is_homework_question(question: str) -> bool:
    text = question.lower()
    return any(re.search(p, text) for p in HOMEWORK_PATTERNS)