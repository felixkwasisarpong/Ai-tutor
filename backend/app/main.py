import os
from fastapi import FastAPI, Request
import uuid

from app.rag.store import vector_store
from app.rag.ingest import load_pdf, chunk_text,make_chunks
from app.api.ask import router as ask_router
from app.core.config import settings
from app.health import router as health_router
from app.api.admin import router as admin_router
from app.core.middleware.request_id import RequestIdMiddleware
from app.core.logging import setup_logging


app = FastAPI(title=settings.app_name)
app.add_middleware(RequestIdMiddleware)
setup_logging()
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


app.include_router(health_router)
app.include_router(ask_router)
app.include_router(admin_router)
app.include_router(health_router)
PDF_PATH = "/app/data/L3-knowledgebase.pdf"
DOCUMENTS = [
    {
        "path": "/app/data/L3-knowledgebase.pdf",
        "course": "Intelligent Systems",
        "document": "L3-knowledgebase.pdf",
    },
    {
        "path": "/app/data/09 Gathering and Processing Data - Model Evaluation.pdf",
        "course": "Applied Datascience",
        "document": "Model Evaluation",
    },
]

@app.on_event("startup")
def load_vector_store():
    if vector_store.index.ntotal > 0:
        print(
            f"✅ RAG store loaded with {vector_store.index.ntotal} vectors"
        )
    else:
        print("⚠️ RAG store is empty — awaiting admin ingestion")