from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.models.ask import AskRequest
from app.llm.prompts import default_prompt
from app.llm.client import OllamaClient
from app.core.logging import logger
from app.rag.retrieve import retrieve_context
from app.agent.graph import build_agent
from app.core.course_registry import get_course_by_code

agent = build_agent()
router = APIRouter()
llm = OllamaClient()

class Citation(BaseModel):
    document: str
    chunk: int | None
    ref: str

class AskRequest(BaseModel):
    question: str
    course_code: str | None = None
class AskResponse(BaseModel):
    answer: str
    source: str
    citations: Optional[List[Citation]] = None






@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:

    if payload.course_code:
        # Optional validation (kept, but now meaningful)
        get_course_by_code(payload.course_code)
        print("ASK PAYLOAD:", payload)
        result = agent.invoke({
            "question": payload.question,
            "force_rag": True,
            "course_code": payload.course_code,
        })
    else:
        result = agent.invoke({
            "question": payload.question,
            "force_rag": False,
        })

    return {
        "answer": result["answer"],
        "source": result["source"],
        "citations": result.get("citations"),
    }


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
