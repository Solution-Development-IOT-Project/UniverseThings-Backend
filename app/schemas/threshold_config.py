from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class ThresholdConfigBase(BaseModel):
    # Tipo de parámetro monitoreado: temperature, humidity, ph, ndvi, etc.
    parameter: str

    # Umbrales principales
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    # Umbrales de advertencia
    warn_min: Optional[float] = None
    warn_max: Optional[float] = None

    is_active: bool = True

    # >, <, >=, <=, between, etc.
    operator: str = "between"

    # FKs
    sensor_id: int
    zone_id: int


# -----------------------
# CREATE
# -----------------------
class ThresholdConfigCreate(ThresholdConfigBase):
    pass


# -----------------------
# UPDATE
# -----------------------
class ThresholdConfigUpdate(BaseModel):
    parameter: Optional[str] = None

    min_value: Optional[float] = None
    max_value: Optional[float] = None

    warn_min: Optional[float] = None
    warn_max: Optional[float] = None

    is_active: Optional[bool] = None
    operator: Optional[str] = None

    sensor_id: Optional[int] = None
    zone_id: Optional[int] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class ThresholdConfigInDBBase(ThresholdConfigBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class ThresholdConfig(ThresholdConfigInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class ThresholdConfigInDB(ThresholdConfigInDBBase):
    pass
