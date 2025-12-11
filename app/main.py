from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.routers import warranty, users, auth, ui
from app.database import Base, engine
from app.core.config import settings

# Create DB tables on startup (simple approach for this task)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eport Warranty Register API",
    version="1.0.0",
    description="API for registering device warranties and listing registered assets."
)

# Session middleware for Warranty Centre UI
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

# API routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(warranty.router)

# UI routes
app.include_router(ui.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Warranty Register API online"}

