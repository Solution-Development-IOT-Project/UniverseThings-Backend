from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.notification import Notification as NotificationModel
from app.models.user import User
from app.schemas.notification import (
    Notification as NotificationSchema,
    NotificationCreate,
    NotificationUpdate,
)

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)


# -----------------------
# LISTAR NOTIFICACIONES DEL USUARIO ACTUAL
# -----------------------
@router.get("/", response_model=List[NotificationSchema])
def list_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(NotificationModel)
        .filter(NotificationModel.user_id == current_user.id)
        .order_by(NotificationModel.created_at.desc())
        .all()
    )


# -----------------------
# OBTENER UNA NOTIFICACIÓN
# -----------------------
@router.get("/{notification_id}", response_model=NotificationSchema)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    obj = (
        db.query(NotificationModel)
        .filter(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == current_user.id,
        )
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada",
        )
    return obj


# -----------------------
# CREAR (normalmente desde backend/servicio)
# -----------------------
@router.post("/", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED)
def create_notification(
    n_in: NotificationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    obj = NotificationModel(**n_in.dict(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ACTUALIZAR
# -----------------------
@router.put("/{notification_id}", response_model=NotificationSchema)
def update_notification(
    notification_id: int,
    n_in: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    obj = (
        db.query(NotificationModel)
        .filter(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == current_user.id,
        )
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada",
        )

    data = n_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# MARCAR COMO LEÍDA
# -----------------------
@router.post("/{notification_id}/read", response_model=NotificationSchema)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    obj = (
        db.query(NotificationModel)
        .filter(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == current_user.id,
        )
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada",
        )

    obj.is_read = True
    from datetime import datetime as dt

    obj.read_at = dt.utcnow()
    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ELIMINAR
# -----------------------
@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    obj = (
        db.query(NotificationModel)
        .filter(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == current_user.id,
        )
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada",
        )

    db.delete(obj)
    db.commit()
