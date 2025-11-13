from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class CooperativeBase(BaseModel):
    name: str
    description: Optional[str] = None

    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

    address: Optional[str] = None


# -----------------------
# CREATE
# -----------------------
class CooperativeCreate(CooperativeBase):
    pass


# -----------------------
# UPDATE
# -----------------------
class CooperativeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

    address: Optional[str] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class CooperativeInDBBase(CooperativeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Cooperative(CooperativeInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class CooperativeInDB(CooperativeInDBBase):
    pass
