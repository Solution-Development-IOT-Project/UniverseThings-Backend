from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, Field


# -----------------------
# BASE
# -----------------------
class ImageBase(BaseModel):
    file_path: str
    image_type: str

    # nombre interno: image_metadata
    # nombre en JSON: "metadata"
    image_metadata: Optional[Any] = Field(default=None, alias="metadata")

    analysis_result: Optional[str] = None
    camera_id: int

    # permitir usar nombres internos (image_metadata) y alias
    model_config = ConfigDict(populate_by_name=True)


# -----------------------
# CREATE
# -----------------------
class ImageCreate(ImageBase):
    captured_at: Optional[datetime] = None
    # opcional para imágenes enviadas desde dron o edge device


# -----------------------
# UPDATE
# -----------------------
class ImageUpdate(BaseModel):
    file_path: Optional[str] = None
    image_type: Optional[str] = None

    # igual que en base: interno image_metadata, JSON "metadata"
    image_metadata: Optional[Any] = Field(default=None, alias="metadata")

    analysis_result: Optional[str] = None
    camera_id: Optional[int] = None
    captured_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True)


# -----------------------
# BASE DESDE BD
# -----------------------
class ImageInDBBase(ImageBase):
    id: int
    captured_at: datetime
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# -----------------------
# RESPUESTA API
# -----------------------
class Image(ImageInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class ImageInDB(ImageInDBBase):
    pass
