from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class ParcelBase(BaseModel):
    name: str
    description: Optional[str] = None
    area_hectares: Optional[float] = None

    # Clave foránea obligatoria
    farm_id: int


class ParcelCreate(ParcelBase):
    pass


class ParcelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    area_hectares: Optional[float] = None
    farm_id: Optional[int] = None



class ParcelInDBBase(ParcelBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class Parcel(ParcelInDBBase):
    pass


class ParcelInDB(ParcelInDBBase):
    pass
