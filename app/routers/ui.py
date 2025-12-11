from typing import Optional, List

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, WarrantyRegistration
from app.core.security import verify_password

router = APIRouter(tags=["Warranty Centre UI"])

templates = Jinja2Templates(directory="templates")


def get_current_user_from_session(request: Request, db: Session) -> Optional[User]:
    email = request.session.get("user_email")
    if not email:
        return None
    return db.query(User).filter(User.email == email).first()


@router.get("/warranty/login")
def warranty_login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None},
    )


@router.post("/warranty/login")
def warranty_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid email or password",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.session["user_email"] = user.email
    return RedirectResponse(url="/warranty", status_code=status.HTTP_302_FOUND)


@router.get("/warranty")
def warranty_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user_from_session(request, db)
    if not user:
        return RedirectResponse(url="/warranty/login", status_code=status.HTTP_302_FOUND)

    warranties: List[WarrantyRegistration] = (
        db.query(WarrantyRegistration)
        .order_by(WarrantyRegistration.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user_email": user.email,
            "warranties": warranties,
        },
    )


@router.get("/warranty/logout")
def warranty_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/warranty/login", status_code=status.HTTP_302_FOUND)

