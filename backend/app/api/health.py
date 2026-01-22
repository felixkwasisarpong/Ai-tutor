from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ready")
def readiness():
    return {
        "database": "ok",
        "rag_store": "ok",
    }