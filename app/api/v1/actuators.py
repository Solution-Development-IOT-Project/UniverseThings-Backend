from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.actuator import Actuator as ActuatorModel
from app.schemas.actuator import (
    Actuator as ActuatorSchema,
    ActuatorCreate,
    ActuatorUpdate,
)

router = APIRouter(
    prefix="/actuators",
    tags=["actuators"],
)


# -----------------------
# LISTAR TODOS
# -----------------------
@router.get("/", response_model=List[ActuatorSchema])
def list_actuators(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(ActuatorModel).all()


# -----------------------
# OBTENER POR ID
# -----------------------
@router.get("/{actuator_id}", response_model=ActuatorSchema)
def get_actuator(
    actuator_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ActuatorModel).filter(ActuatorModel.id == actuator_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actuador no encontrado",
        )
    return obj


# -----------------------
# CREAR
# -----------------------
@router.post("/", response_model=ActuatorSchema, status_code=status.HTTP_201_CREATED)
def create_actuator(
    actuator_in: ActuatorCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = ActuatorModel(**actuator_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ACTUALIZAR
# -----------------------
@router.put("/{actuator_id}", response_model=ActuatorSchema)
def update_actuator(
    actuator_id: int,
    actuator_in: ActuatorUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ActuatorModel).filter(ActuatorModel.id == actuator_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actuador no encontrado",
        )

    data = actuator_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ELIMINAR
# -----------------------
@router.delete("/{actuator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actuator(
    actuator_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ActuatorModel).filter(ActuatorModel.id == actuator_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actuador no encontrado",
        )

    db.delete(obj)
    db.commit()


# -----------------------
# ENDPOINT EXTRA: CAMBIAR ESTADO (ON/OFF)
# -----------------------
@router.post("/{actuator_id}/toggle", response_model=ActuatorSchema)
def toggle_actuator_state(
    actuator_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ActuatorModel).filter(ActuatorModel.id == actuator_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actuador no encontrado",
        )

    obj.is_on = not obj.is_on
    db.commit()
    db.refresh(obj)
    return obj
