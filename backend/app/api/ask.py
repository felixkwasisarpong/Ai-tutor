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
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.service.courses import get_course_by_code
from fastapi import HTTPException

agent = build_agent()
router = APIRouter()
llm = OllamaClient()


class Citation(BaseModel):
    document: str
    chunk: int | None
    ref: str | None = None


class AskRequest(BaseModel):
    question: str
    course_code: str | None = None


class AskResponse(BaseModel):
    answer: str
    source: str
    citations: List[Citation] = []
    confidence: str


@router.post("/ask", response_model=AskResponse)
def ask_question(
    payload: AskRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> AskResponse:
    request_id = request.state.request_id

    logger.info(
        "ASK request received",
        extra={
            "request_id": request_id,
            "course_code": payload.course_code,
            "question": payload.question,
        },
    )

    if payload.course_code:
        course = get_course_by_code(db, payload.course_code)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        result = agent.invoke({
            "question": payload.question,
            "force_rag": True,
            "course_code": payload.course_code,
            "request_id": request_id,
        })

        if result["source"].startswith("rag") and result.get("citations") is None:
            raise HTTPException(
                status_code=500,
                detail="Invariant violation: RAG response missing citations",
            )
    else:
        result = agent.invoke({
            "question": payload.question,
            "force_rag": False,
            "request_id": request_id,
        })

    return {
        "answer": result["answer"],
        "source": result["source"],
        "citations": result.get("citations", []),
        "confidence": result.get("confidence", "none"),
    }

@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
