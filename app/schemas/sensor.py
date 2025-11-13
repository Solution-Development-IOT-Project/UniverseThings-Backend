from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class SensorBase(BaseModel):
    name: str
    sensor_type: str
    model: Optional[str] = None
    unit: Optional[str] = None
    is_active: bool = True

    # FK obligatoria
    zone_id: int


# -----------------------
# CREATE
# -----------------------
class SensorCreate(SensorBase):
    pass


# -----------------------
# UPDATE
# -----------------------
class SensorUpdate(BaseModel):
    name: Optional[str] = None
    sensor_type: Optional[str] = None
    model: Optional[str] = None
    unit: Optional[str] = None
    is_active: Optional[bool] = None
    zone_id: Optional[int] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class SensorInDBBase(SensorBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Sensor(SensorInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class SensorInDB(SensorInDBBase):
    pass
