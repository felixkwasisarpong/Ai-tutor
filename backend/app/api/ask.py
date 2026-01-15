from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/ask", tags=["ask"])


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    answer = f"You asked: {payload.question}"
    return AskResponse(answer=answer)
