from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict

class CultivationZoneBase(BaseModel):
    name: str
    crop_type: Optional[str] = None
    description: Optional[str] = None
    area_m2: Optional[float] = None

    # FK obligatoria
    parcel_id: int


class CultivationZoneCreate(CultivationZoneBase):
    pass


class CultivationZoneUpdate(BaseModel):
    name: Optional[str] = None
    crop_type: Optional[str] = None
    description: Optional[str] = None
    area_m2: Optional[float] = None
    parcel_id: Optional[int] = None


class CultivationZoneInDBBase(CultivationZoneBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CultivationZone(CultivationZoneInDBBase):
    pass

class CultivationZoneInDB(CultivationZoneInDBBase):
    pass
