from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.prompts import default_prompt
from app.llm.client import OllamaClient
from app.core.logging import logger
from app.rag.retrieve import retrieve_context

router = APIRouter()
llm = OllamaClient()

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    source: str


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    context = retrieve_context(payload.question)
    prompt = f"""
            You are a university-level science tutor.
            Use the context below to answer accurately.

            Context:
            {context}

            Question:
            {payload.question}

            Answer:
            """.strip()

    answer = llm.generate(prompt)

    return AskResponse(
        answer=answer,
        source="rag+ollama"
    )


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
