import os
from fastapi import FastAPI
from app.rag.store import vector_store
from app.rag.ingest import load_pdf, chunk_text,make_chunks
from app.api.ask import router as ask_router
from app.core.config import settings
from app.health import router as health_router



app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(ask_router)
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
def load_rag_data():
    if vector_store.index.ntotal > 0:
        print("RAG already loaded from disk, skipping ingestion")
        return

    for doc in DOCUMENTS:
        if not os.path.exists(doc["path"]):
            print(f"Missing RAG file: {doc['path']}")
            continue

        text = load_pdf(doc["path"])
        chunks = make_chunks(
            chunk_text(text),
            course=doc["course"],
            document=doc["document"],
        )

        vector_store.add(chunks)
        print(f"Loaded {len(chunks)} chunks from {doc['document']}")