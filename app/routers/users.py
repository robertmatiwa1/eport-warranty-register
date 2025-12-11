from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.core.security import hash_password

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Provision a new Warranty Centre user.
    In a real environment this would be restricted to admins.
    """
    hashed_pw = hash_password(payload.password)
    user = User(email=payload.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

