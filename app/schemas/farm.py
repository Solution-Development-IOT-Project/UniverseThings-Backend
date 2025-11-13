from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class FarmBase(BaseModel):
    name: str
    location: Optional[str] = None
    description: Optional[str] = None


class FarmCreate(FarmBase):
    pass


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class FarmInDBBase(FarmBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Farm(FarmInDBBase):
    pass

class FarmInDB(FarmInDBBase):
    pass
