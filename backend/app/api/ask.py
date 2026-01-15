from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.prompts import default_prompt
from app.llm.client import OllamaClient



router = APIRouter()
llm = OllamaClient()

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    source: str


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    prompt = default_prompt(payload.question)
    answer = llm.generate(prompt)

    return AskResponse(answer=answer, source="ollama:llama3")


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
