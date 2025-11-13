from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class AutomationLogBase(BaseModel):
    status: str = "triggered"        # triggered, skipped, failed
    message: Optional[str] = None
    details: Optional[str] = None
    action_executed: bool = False

    # FKs (algunos opcionales)
    rule_id: int
    actuator_id: Optional[int] = None
    sensor_id: Optional[int] = None
    zone_id: Optional[int] = None


# -----------------------
# CREATE
# -----------------------
class AutomationLogCreate(AutomationLogBase):
    executed_at: Optional[datetime] = None


# -----------------------
# UPDATE
# -----------------------
class AutomationLogUpdate(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None
    action_executed: Optional[bool] = None

    rule_id: Optional[int] = None
    actuator_id: Optional[int] = None
    sensor_id: Optional[int] = None
    zone_id: Optional[int] = None

    executed_at: Optional[datetime] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class AutomationLogInDBBase(AutomationLogBase):
    id: int
    created_at: Optional[datetime]
    executed_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class AutomationLog(AutomationLogInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class AutomationLogInDB(AutomationLogInDBBase):
    pass
