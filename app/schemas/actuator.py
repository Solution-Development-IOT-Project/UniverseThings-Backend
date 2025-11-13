from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class ActuatorBase(BaseModel):
    name: str
    actuator_type: str
    model: Optional[str] = None

    is_on: bool = False
    auto_mode: bool = True

    # FK obligatoria
    zone_id: int


class ActuatorCreate(ActuatorBase):
    pass


class ActuatorUpdate(BaseModel):
    name: Optional[str] = None
    actuator_type: Optional[str] = None
    model: Optional[str] = None
    is_on: Optional[bool] = None
    auto_mode: Optional[bool] = None
    zone_id: Optional[int] = None


class ActuatorInDBBase(ActuatorBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Actuator(ActuatorInDBBase):
    pass


class ActuatorInDB(ActuatorInDBBase):
    pass
