from app.llm.client import OllamaClient

llm = OllamaClient()

ROUTER_PROMPT = """
You are an AI router for a university tutor system.

Decide whether the user's question requires consulting course documents
(such as lecture notes, PDFs, slides, or a knowledgebase),
or if it can be answered using general knowledge.

Rules:
- Answer ONLY with JSON
- Do NOT answer the question itself
- Default to "false" unless document context is clearly useful

Respond in this format:
{{
  "use_rag": true | false,
  "reason": "<short explanation>"
}}

Question:
{question}
""".strip()


def route_question(question: str) -> dict:
    prompt = ROUTER_PROMPT.format(question=question)
    response = llm.generate(
        ROUTER_PROMPT.format(question=question)
    )


    try:
       import json
       result = json.loads(response)
       return {
              "use_rag": bool(result.get("use_rag", False)),
              "reason": result.get("reason", "")
       }
    except Exception:
         return {
              "use_rag": False,
              "reason": "Failed to parse router output"
         }