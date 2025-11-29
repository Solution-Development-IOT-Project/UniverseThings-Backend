from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.cultivation_zone import CultivationZone as ZoneModel
from app.schemas.cultivation_zone import (
    CultivationZone as ZoneSchema,
    CultivationZoneCreate,
    CultivationZoneUpdate,
)
from app.crud.crud_parcel import parcel as crud_parcel
from app.crud.crud_cultivation_zone import cultivation_zone as crud_cultivation_zone

router = APIRouter(
    prefix="/zones",
    tags=["cultivation_zones"],
)


@router.get("/", response_model=List[ZoneSchema])
def list_zones(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(ZoneModel).all()


@router.get("/{zone_id}", response_model=ZoneSchema)
def get_zone(
    zone_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ZoneModel).filter(ZoneModel.id == zone_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zona no encontrada",
        )
    return obj


@router.post("/", response_model=ZoneSchema, status_code=status.HTTP_201_CREATED)
def create_zone(
    zone_in: CultivationZoneCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    # Validate parcel_id
    if zone_in.parcel_id is not None:
        existing_parcel = crud_parcel.get(db, id=zone_in.parcel_id)
        if not existing_parcel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parcel with ID {zone_in.parcel_id} not found."
            )

    obj = crud_cultivation_zone.create(db, obj_in=zone_in)
    return obj


@router.put("/{zone_id}", response_model=ZoneSchema)
def update_zone(
    zone_id: int,
    zone_in: CultivationZoneUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ZoneModel).filter(ZoneModel.id == zone_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zona no encontrada",
        )

    data = zone_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(
    zone_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ZoneModel).filter(ZoneModel.id == zone_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zona no encontrada",
        )

    db.delete(obj)
    db.commit()
