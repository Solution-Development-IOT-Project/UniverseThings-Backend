from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class AlertBase(BaseModel):
    message: str
    details: Optional[str] = None

    # info, warning, critical
    severity: str = "info"

    is_read: bool = False

    # FK obligatoria a zona
    zone_id: int

    # FK opcional a sensor
    sensor_id: Optional[int] = None


# -----------------------
# CREATE
# -----------------------
class AlertCreate(AlertBase):
    # En caso quieras registrar la fecha de creación/levantamiento
    created_at: Optional[datetime] = None


# -----------------------
# UPDATE
# -----------------------
class AlertUpdate(BaseModel):
    message: Optional[str] = None
    details: Optional[str] = None
    severity: Optional[str] = None
    is_read: Optional[bool] = None
    zone_id: Optional[int] = None
    sensor_id: Optional[int] = None
    resolved_at: Optional[datetime] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class AlertInDBBase(AlertBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Alert(AlertInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class AlertInDB(AlertInDBBase):
    pass
