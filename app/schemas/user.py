from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    is_active: bool = True
    role_id: Optional[int] = None

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


class UserInDBBase(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Para permitir .from_orm() / from_attributes (Pydantic v2)
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    """Schema para respuestas de la API (no expone password)."""
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
