from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


# -----------------------
# BASE
# -----------------------
class NotificationBase(BaseModel):
    title: str
    message: str

    # alert, automation, report, device, system
    notification_type: str = "alert"

    is_read: bool = False

    # push, email, sms, internal
    channel: Optional[str] = None

    # Usuario que recibe la notificación
    user_id: int

    # Relaciones opcionales
    alert_id: Optional[int] = None
    sensor_id: Optional[int] = None
    actuator_id: Optional[int] = None
    zone_id: Optional[int] = None


# -----------------------
# CREATE
# -----------------------
class NotificationCreate(NotificationBase):
    read_at: Optional[datetime] = None


# -----------------------
# UPDATE
# -----------------------
class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    notification_type: Optional[str] = None
    is_read: Optional[bool] = None
    channel: Optional[str] = None

    user_id: Optional[int] = None
    alert_id: Optional[int] = None
    sensor_id: Optional[int] = None
    actuator_id: Optional[int] = None
    zone_id: Optional[int] = None

    read_at: Optional[datetime] = None


# -----------------------
# BASE DESDE BD
# -----------------------
class NotificationInDBBase(NotificationBase):
    id: int
    created_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# RESPUESTA API
# -----------------------
class Notification(NotificationInDBBase):
    pass


# -----------------------
# INTERNO
# -----------------------
class NotificationInDB(NotificationInDBBase):
    pass
