from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class WarrantyCreate(BaseModel):
    asset_id: str
    asset_name: str
    registered_by: str
