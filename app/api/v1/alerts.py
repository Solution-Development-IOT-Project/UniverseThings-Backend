from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.alert import Alert as AlertModel
from app.schemas.alert import (
    Alert as AlertSchema,
    AlertCreate,
    AlertUpdate,
)

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
)


# -----------------------
# LISTAR TODAS LAS ALERTAS
# -----------------------
@router.get("/", response_model=List[AlertSchema])
def list_alerts(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(AlertModel).order_by(AlertModel.created_at.desc()).all()


# -----------------------
# OBTENER ALERTA POR ID
# -----------------------
@router.get("/{alert_id}", response_model=AlertSchema)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada",
        )
    return obj


# -----------------------
# CREAR ALERTA
# -----------------------
@router.post("/", response_model=AlertSchema, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_in: AlertCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    data = alert_in.dict(exclude_unset=True)
    obj = AlertModel(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ACTUALIZAR ALERTA
# -----------------------
@router.put("/{alert_id}", response_model=AlertSchema)
def update_alert(
    alert_id: int,
    alert_in: AlertUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada",
        )

    data = alert_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ELIMINAR ALERTA
# -----------------------
@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada",
        )

    db.delete(obj)
    db.commit()


# -----------------------
# MARCAR ALERTA COMO LEÍDA
# -----------------------
@router.post("/{alert_id}/read", response_model=AlertSchema)
def mark_alert_as_read(
    alert_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada",
        )

    obj.is_read = True
    db.commit()
    db.refresh(obj)
    return obj
