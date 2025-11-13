from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class DeviceBase(BaseModel):
    name: str
    device_type: str                  # gateway, node, controller, etc.
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None
    is_online: bool = False
    last_seen: Optional[datetime] = None

    zone_id: Optional[int] = None     # puede ser NULL en el modelo


# -----------------------
# CREATE
# -----------------------
class DeviceCreate(DeviceBase):
    pass


# -----------------------
# UPDATE
# -----------------------
class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None
    is_online: Optional[bool] = None
    last_seen: Optional[datetime] = None
    zone_id: Optional[int] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class DeviceInDBBase(DeviceBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Device(DeviceInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class DeviceInDB(DeviceInDBBase):
    pass
