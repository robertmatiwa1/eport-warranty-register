import os
from functools import lru_cache

class Settings:
    PROJECT_NAME: str = "Eport Warranty Register API"

    # Database configuration
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/warranty_db"
    )

    # JWT configuration
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "supersecretjwtkey")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # API key for service-to-service calls (Next.js -> Warranty API)
    API_KEY: str = os.environ.get("API_KEY", "super-secret-api-key")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

