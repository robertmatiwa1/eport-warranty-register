import os

class Settings:
    PROJECT_NAME: str = "Eport Warranty Register API"
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/warranty_db")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "supersecretjwtkey")
    JWT_ALGORITHM: str = "HS256"

settings = Settings()
