from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.device import Device as DeviceModel
from app.schemas.device import (
    Device as DeviceSchema,
    DeviceCreate,
    DeviceUpdate,
)

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


@router.get("/", response_model=List[DeviceSchema])
def list_devices(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(DeviceModel).all()


@router.get("/{device_id}", response_model=DeviceSchema)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    return obj


@router.post("/", response_model=DeviceSchema, status_code=status.HTTP_201_CREATED)
def create_device(
    device_in: DeviceCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = DeviceModel(**device_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{device_id}", response_model=DeviceSchema)
def update_device(
    device_id: int,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )

    data = device_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )

    db.delete(obj)
    db.commit()
