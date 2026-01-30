import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid

from app.rag.store import vector_store

from app.api.ask import router as ask_router
from app.core.config import settings
from app.health import router as health_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.core.middleware.request_id import RequestIdMiddleware
from app.core.logging import setup_logging


app = FastAPI(title=settings.app_name)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_logging()


app.include_router(health_router)
app.include_router(ask_router)
app.include_router(admin_router)
app.include_router(auth_router)



@app.on_event("startup")
def load_vector_store():
    if vector_store.index.ntotal > 0:
        print(
            f"✅ RAG store loaded with {vector_store.index.ntotal} vectors"
        )
    else:
        print("⚠️ RAG store is empty — awaiting admin ingestion")
