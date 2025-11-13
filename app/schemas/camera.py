from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class CameraBase(BaseModel):
    name: str
    camera_type: str                     # RGB, NDVI, thermal, etc.
    model: Optional[str] = None
    is_active: bool = True
    location_description: Optional[str] = None

    # FK obligatoria
    zone_id: int


# -----------------------
# CREATE
# -----------------------
class CameraCreate(CameraBase):
    pass


# -----------------------
# UPDATE
# -----------------------
class CameraUpdate(BaseModel):
    name: Optional[str] = None
    camera_type: Optional[str] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None
    location_description: Optional[str] = None
    zone_id: Optional[int] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class CameraInDBBase(CameraBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Camera(CameraInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class CameraInDB(CameraInDBBase):
    pass
