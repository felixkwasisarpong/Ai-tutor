from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/ask", tags=["ask"])


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    source: str


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    answer = f"You asked: {payload.question}"
    return AskResponse(answer=f"You asked: {payload.question}", source="placeholder")


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
