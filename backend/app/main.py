from fastapi import FastAPI
from app.rag.store import vector_store
from app.rag.ingest import load_pdf, chunk_text
from app.api.ask import router as ask_router
from app.core.config import settings
from app.health import router as health_router


app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(ask_router)


@app.on_event("startup")
def load_rag_data():
    try:
        text = load_pdf("/app/data/L3-knowledgebase.pdf")
        chunks = chunk_text(text)
        vector_store.add(chunks)
        print(f"Loaded {len(chunks)} RAG chunks")
    except Exception as e:
        print(f"RAG not loaded: {e}")