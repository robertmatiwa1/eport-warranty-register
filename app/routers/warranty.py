from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models import WarrantyRegistration, User
from app.schemas import WarrantyCreate, WarrantyOut
from app.core.security import verify_api_key, decode_token

router = APIRouter(prefix="/api/warranty", tags=["Warranty"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    email = decode_token(token)
    user = db.query(User).filter(User.email == email).first()
    return user


@router.post("/register", response_model=WarrantyOut, dependencies=[Depends(verify_api_key)])
def register_warranty(
    payload: WarrantyCreate,
    db: Session = Depends(get_db),
):
    """
    Register a warranty for an asset.
    This endpoint is protected by an API key and is intended to be called
    from the Next.js Asset Manager application.
    """
    entry = WarrantyRegistration(**payload.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/list", response_model=List[WarrantyOut])
def list_warranties(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all registered warranties.
    Access controlled via JWT (Warranty Centre users).
    """
    return db.query(WarrantyRegistration).order_by(WarrantyRegistration.created_at.desc()).all()

