from fastapi import APIRouter
from pydantic import BaseModel

from app.llm.prompts import default_prompt
from app.llm.client import OllamaClient
from app.core.logging import logger
from app.rag.retrieve import retrieve_context
from app.agent.graph import build_agent

agent = build_agent()
router = APIRouter()
llm = OllamaClient()

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    source: str


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    result = agent.invoke({
        "question": payload.question,
        "use_rag": False,
        "context": None,
        "answer": None
    })  

    return AskResponse(
        answer=result["answer"],
        source="agent+rag" if result["use_rag"] else "agent"
    )


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
