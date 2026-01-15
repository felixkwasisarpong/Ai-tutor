from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "ai-tutor-backend"
    environment: str = os.getenv("ENVIRONMENT", "local")
    log_level: str = os.getenv("LOG_LEVEL", "info")


settings = Settings()
