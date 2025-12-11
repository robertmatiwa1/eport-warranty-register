from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WarrantyRegistration(Base):
    __tablename__ = "warranty_registrations"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, index=True)
    asset_name = Column(String)
    registered_by = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
