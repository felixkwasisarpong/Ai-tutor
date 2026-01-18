from app.llm.client import OllamaClient
import json
import re
llm = OllamaClient()

ROUTER_PROMPT = """
You are a routing function, not a chatbot.

Your job is to decide whether a user's question requires consulting
course documents (lecture notes, PDFs, slides, knowledgebases).

Rules (MANDATORY):
- Respond with VALID JSON only
- Do not include markdown
- Do not include explanations outside JSON
- Do not include backticks
- Do not include extra text

JSON schema (MUST MATCH EXACTLY):
{{
  "use_rag": true | false,
  "reason": "short explanation"
}}

Default behavior:
- If unsure, set "use_rag" to false

User question:
{question}
""".strip()
COURSE_HINT_KEYWORDS = [
    "this course",
    "our course",
    "the course",
    "lecture",
    "slides",
    "notes",
    "in class",
]


def route_question(question: str) -> dict:
    q = question.lower()
    if any(k in q for k in COURSE_HINT_KEYWORDS):
        return {
            "use_rag": True,
            "reason": "Explicit course reference detected",
        }
    response = llm.generate(
        ROUTER_PROMPT.format(question=question)
    )

    if response.startswith("Error:"):
        print(f"ROUTER LLM ERROR → {response}")
        return {
            "use_rag": False,
            "reason": "Router LLM error",
        }

    try:
        # Extract first JSON object defensively
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found")

        result = json.loads(match.group())

        return {
            "use_rag": bool(result.get("use_rag", False)),
            "reason": result.get("reason", "No reason provided"),
        }

    except Exception as e:
        print(f"ROUTER PARSE ERROR → {e} | raw={response!r}")
        return {
            "use_rag": False,
            "reason": "Failed to parse router output",
        }
