from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"



class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None


class AuthUser(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role_id: Optional[int]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
