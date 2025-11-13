from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class AutomationRuleBase(BaseModel):
    name: str
    is_active: bool = True
    priority: int = 1

    # condición en formato texto/JSON
    # Ej: {"sensor_id": 3, "operator": ">", "value": 30}
    condition: str

    # descripción opcional de la acción
    action_description: Optional[str] = None

    # FK obligatoria a zona
    zone_id: int


# -----------------------
# CREATE
# -----------------------
class AutomationRuleCreate(AutomationRuleBase):
    pass


# -----------------------
# UPDATE
# -----------------------
class AutomationRuleUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    condition: Optional[str] = None
    action_description: Optional[str] = None
    zone_id: Optional[int] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class AutomationRuleInDBBase(AutomationRuleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class AutomationRule(AutomationRuleInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class AutomationRuleInDB(AutomationRuleInDBBase):
    pass
