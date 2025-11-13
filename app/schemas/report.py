from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None

    # Tipo de reporte: sensor_summary, ndvi_analysis, alerts_history, etc.
    report_type: str

    # Ruta del archivo generado (PDF, CSV, Excel, etc.)
    file_path: Optional[str] = None

    # generated, failed, pending
    status: str = "generated"

    # Contexto agrícola
    farm_id: Optional[int] = None
    parcel_id: Optional[int] = None
    zone_id: Optional[int] = None

    # Usuario que lo generó
    created_by_id: Optional[int] = None


# -----------------------
# CREATE
# -----------------------
class ReportCreate(ReportBase):
    generated_at: Optional[datetime] = None
    # Opcional si el servicio genera la fecha manualmente


# -----------------------
# UPDATE
# -----------------------
class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    report_type: Optional[str] = None
    file_path: Optional[str] = None
    status: Optional[str] = None

    farm_id: Optional[int] = None
    parcel_id: Optional[int] = None
    zone_id: Optional[int] = None

    created_by_id: Optional[int] = None
    generated_at: Optional[datetime] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class ReportInDBBase(ReportBase):
    id: int
    generated_at: Optional[datetime] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Report(ReportInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class ReportInDB(ReportInDBBase):
    pass
