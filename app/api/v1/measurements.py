from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.measurement import Measurement as MeasurementModel
from app.schemas.measurement import (
    Measurement as MeasurementSchema,
    MeasurementCreate,
    MeasurementUpdate,
)

router = APIRouter(
    prefix="/measurements",
    tags=["measurements"],
)


@router.get("/", response_model=List[MeasurementSchema])
def list_measurements(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
    limit: int = 200,
):
    q = (
        db.query(MeasurementModel)
        .order_by(MeasurementModel.timestamp.desc())
        .limit(limit)
    )
    return q.all()


@router.get("/{measurement_id}", response_model=MeasurementSchema)
def get_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = (
        db.query(MeasurementModel)
        .filter(MeasurementModel.id == measurement_id)
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medición no encontrada",
        )
    return obj


@router.post("/", response_model=MeasurementSchema, status_code=status.HTTP_201_CREATED)
def create_measurement(
    m_in: MeasurementCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = MeasurementModel(**m_in.dict(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{measurement_id}", response_model=MeasurementSchema)
def update_measurement(
    measurement_id: int,
    m_in: MeasurementUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = (
        db.query(MeasurementModel)
        .filter(MeasurementModel.id == measurement_id)
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medición no encontrada",
        )

    data = m_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = (
        db.query(MeasurementModel)
        .filter(MeasurementModel.id == measurement_id)
        .first()
    )
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medición no encontrada",
        )

    db.delete(obj)
    db.commit()
