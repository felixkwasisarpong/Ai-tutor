from fastapi import FastAPI

from app.api.ask import router as ask_router
from app.core.config import settings
from app.health import router as health_router


app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(ask_router)
