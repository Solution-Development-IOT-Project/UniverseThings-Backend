from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class ImageBase(BaseModel):
    file_path: str                       # ruta donde está almacenada la imagen
    image_type: str                      # rgb, ndvi, thermal, segmentation, etc.
    metadata: Optional[str] = None       # metadatos en formato texto/JSON
    analysis_result: Optional[str] = None

    camera_id: int                       # FK obligatoria


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
    metadata: Optional[str] = None
    analysis_result: Optional[str] = None
    camera_id: Optional[int] = None
    captured_at: Optional[datetime] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class ImageInDBBase(ImageBase):
    id: int
    captured_at: datetime
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


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
