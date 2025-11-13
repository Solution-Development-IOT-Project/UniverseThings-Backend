from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.threshold_config import ThresholdConfig as ThresholdModel
from app.schemas.threshold_config import (
    ThresholdConfig as ThresholdSchema,
    ThresholdConfigCreate,
    ThresholdConfigUpdate,
)

router = APIRouter(
    prefix="/threshold-configs",
    tags=["threshold_configs"],
)


@router.get("/", response_model=List[ThresholdSchema])
def list_threshold_configs(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(ThresholdModel).all()


@router.get("/{config_id}", response_model=ThresholdSchema)
def get_threshold_config(
    config_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ThresholdModel).filter(ThresholdModel.id == config_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de umbral no encontrada",
        )
    return obj


@router.post("/", response_model=ThresholdSchema, status_code=status.HTTP_201_CREATED)
def create_threshold_config(
    t_in: ThresholdConfigCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = ThresholdModel(**t_in.dict(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{config_id}", response_model=ThresholdSchema)
def update_threshold_config(
    config_id: int,
    t_in: ThresholdConfigUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ThresholdModel).filter(ThresholdModel.id == config_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de umbral no encontrada",
        )

    data = t_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_threshold_config(
    config_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ThresholdModel).filter(ThresholdModel.id == config_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración de umbral no encontrada",
        )

    db.delete(obj)
    db.commit()
