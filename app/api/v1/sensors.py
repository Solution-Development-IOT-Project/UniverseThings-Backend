from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.sensor import Sensor as SensorModel
from app.models.measurement import Measurement as MeasurementModel
from app.schemas.sensor import (
    Sensor as SensorSchema,
    SensorCreate,
    SensorUpdate,
)
from app.schemas.measurement import Measurement as MeasurementSchema

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


# -----------------------
# LISTAR TODOS
# -----------------------
@router.get("/", response_model=List[SensorSchema])
def list_sensors(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(SensorModel).all()


# -----------------------
# OBTENER POR ID
# -----------------------
@router.get("/{sensor_id}", response_model=SensorSchema)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor no encontrado",
        )
    return obj


# -----------------------
# CREAR
# -----------------------
@router.post("/", response_model=SensorSchema, status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor_in: SensorCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = SensorModel(**sensor_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ACTUALIZAR
# -----------------------
@router.put("/{sensor_id}", response_model=SensorSchema)
def update_sensor(
    sensor_id: int,
    sensor_in: SensorUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor no encontrado",
        )

    data = sensor_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


# -----------------------
# ELIMINAR
# -----------------------
@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor no encontrado",
        )

    db.delete(obj)
    db.commit()


# -----------------------
# EXTRA: MEDICIONES RECIENTES DEL SENSOR
# -----------------------
@router.get(
    "/{sensor_id}/measurements",
    response_model=List[MeasurementSchema],
)
def list_sensor_measurements(
    sensor_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    sensor = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor no encontrado",
        )

    q = (
        db.query(MeasurementModel)
        .filter(MeasurementModel.sensor_id == sensor_id)
        .order_by(MeasurementModel.timestamp.desc())
        .limit(limit)
    )
    return q.all()
