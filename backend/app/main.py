import os
from fastapi import FastAPI
from app.rag.store import vector_store
from app.rag.ingest import load_pdf, chunk_text
from app.api.ask import router as ask_router
from app.core.config import settings
from app.health import router as health_router


app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(ask_router)
PDF_PATH = "/app/data/L3-knowledgebase.pdf"

@app.on_event("startup")
def load_rag_data():
    if vector_store.index.ntotal > 0:
        print("RAG already loaded from disk,skipping ingestion.")
        return
    
    if not os.path.exists(PDF_PATH):
        print(f"PDF file not found at {PDF_PATH}, skipping RAG ingestion.")
        return
    
    text = load_pdf(PDF_PATH)
    chunks = chunk_text(text)
    vector_store.add(chunks)
    print(f"Loaded {len(chunks)} RAG chuncks fromm {PDF_PATH}")