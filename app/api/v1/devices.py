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
from app.crud.crud_device import device as crud_device
from app.crud.crud_cultivation_zone import cultivation_zone as crud_cultivation_zone

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


@router.get("/", response_model=List[DeviceSchema])
def list_devices(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return crud_device.get_multi(db)


@router.get("/{device_id}", response_model=DeviceSchema)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = crud_device.get(db, id=device_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )
    return obj


@router.post("/", response_model=DeviceSchema, status_code=status.HTTP_201_CREATED)
def create_device(
    device_in: DeviceCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    # Validate zone_id
    if device_in.zone_id is not None:
        existing_zone = crud_cultivation_zone.get(db, id=device_in.zone_id)
        if not existing_zone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cultivation zone with ID {device_in.zone_id} not found."
            )

    obj = crud_device.create(db, obj_in=device_in)
    return obj


@router.put("/{device_id}", response_model=DeviceSchema)
def update_device(
    device_id: int,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = crud_device.get(db, id=device_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    obj = crud_device.update(db, db_obj=obj, obj_in=device_in)
    return obj


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = crud_device.get(db, id=device_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    crud_device.remove(db, id=device_id)
    return {"message": "Device deleted successfully"}