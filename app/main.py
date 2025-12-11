from fastapi import FastAPI
from app.routers import warranty, users
from app.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eport Warranty Register API",
    version="1.0.0",
    description="API for registering device warranties and listing registered assets."
)

app.include_router(users.router)
app.include_router(warranty.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Warranty Register API online"}
