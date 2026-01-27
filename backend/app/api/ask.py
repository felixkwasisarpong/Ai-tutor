from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.prompts import default_prompt
from app.llm.client import OllamaClient
from app.rag.retrieve import retrieve_context
from app.agent.graph import build_agent
from app.core.course_registry import get_course_by_code
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.db.deps import get_db, require_student
from app.service.courses import get_course_by_code
from fastapi import HTTPException
from typing import Literal
from app.core.logging import logger
from app.input.normalize import normalize_input
from fastapi import File, UploadFile, Form
from fastapi import Body



agent = build_agent()
router = APIRouter()
llm = OllamaClient()


class Citation(BaseModel):
    document: str
    chunk: int | None
    ref: str | None = None


class AskResponse(BaseModel):
    answer: str
    source: str
    citations: Optional[List[Citation]] = None
    confidence: Literal["high", "medium", "low", "none"]
    follow_up: Optional[str] = None

@router.post(
    "/ask",
    response_model=AskResponse,
    dependencies=[Depends(require_student)],
)
def ask_question(
    request: Request,
    file: Optional[UploadFile] = File(None),
    question: str = Form(...),
    course_code: str | None = Form(None),
    db: Session = Depends(get_db),
) -> AskResponse:
    request_id = request.state.request_id

    normalized = normalize_input(
        question=question,
        file=file,
    )

    logger.info(
        "ASK request received",
        extra={
            "request_id": request_id,
            "course_code": course_code,
            "question": question,
            "modality": normalized["modality"],
        },
    )

    if course_code:
        course = get_course_by_code(db, course_code)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        result = agent.invoke({
            "question": normalized["question"],
            "extra_context": normalized["context_text"],
            "modality": normalized["modality"],
            "force_rag": True,
            "course_code": course_code,
            "request_id": request_id,
        })

        if (
            result["source"].startswith("rag")
            and result.get("confidence") != "none"
            and not result.get("citations")
        ):
            raise HTTPException(
                status_code=500,
                detail="Invariant violation: RAG response missing citations",
            )
    else:
        result = agent.invoke({
            "question": normalized["question"],
            "force_rag": False,
            "request_id": request_id,
        })

    return {
        "answer": result["answer"],
        "source": result["source"],
        "citations": result.get("citations", []),
        "confidence": result.get("confidence", "none"),
        "follow_up": result.get("follow_up"),
    }

@router.post("/transcribe")
def transcribe_audio(
    request: Request,
    audio: bytes = Body(...)
):
    """
Accepts raw audio bytes from live recording.
Returns transcribed text.
"""
# Placeholder (Phase 6B.4.3)
    raise HTTPException(
        status_code=501,
        detail="Live speech transcription not yet configured",
    )


@router.post("/ocr")
async def extract_text_from_image(
    
    image: UploadFile = File(...),
):
    """
Extract text from an image.
"""
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")


    raise HTTPException(
        status_code=501,
        detail="Image OCR not yet configured",
    )




@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
