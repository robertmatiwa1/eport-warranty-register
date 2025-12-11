from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WarrantyRegistration
from app.schemas import WarrantyCreate

router = APIRouter(prefix="/api/warranty", tags=["Warranty"])

@router.post("/register")
def register_warranty(payload: WarrantyCreate, db: Session = Depends(get_db)):
    entry = WarrantyRegistration(**payload.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"status": "success", "warranty_id": entry.id}

@router.get("/list")
def list_warranties(db: Session = Depends(get_db)):
    return db.query(WarrantyRegistration).all()
