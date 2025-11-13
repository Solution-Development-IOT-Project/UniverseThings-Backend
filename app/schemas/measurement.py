from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class MeasurementBase(BaseModel):
    value: float
    unit: Optional[str] = None
    status: Optional[str] = None  # normal, warning, critical, etc.

    sensor_id: int



class MeasurementCreate(MeasurementBase):
    # Permite opcionalmente inyectar timestamp personalizado
    timestamp: Optional[datetime] = None


class MeasurementUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    sensor_id: Optional[int] = None
    timestamp: Optional[datetime] = None



class MeasurementInDBBase(MeasurementBase):
    id: int
    timestamp: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Measurement(MeasurementInDBBase):
    pass


class MeasurementInDB(MeasurementInDBBase):
    pass
