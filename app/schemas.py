from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class WarrantyCreate(BaseModel):
    asset_id: str
    asset_name: str
    registered_by: str


class WarrantyOut(BaseModel):
    id: int
    asset_id: str
    asset_name: str
    registered_by: str
    created_at: datetime

    class Config:
        from_attributes = True

