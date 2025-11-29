from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.parcel import Parcel
from app.schemas.parcel import Parcel as ParcelSchema, ParcelCreate, ParcelUpdate

router = APIRouter(prefix="/parcels", tags=["parcels"])


@router.get("/", response_model=List[ParcelSchema])
def list_parcels(db: Session = Depends(get_db), _: any = Depends(get_current_active_user)):
    return db.query(Parcel).all()


@router.get("/{parcel_id}", response_model=ParcelSchema)
def get_parcel(parcel_id: int, db: Session = Depends(get_db), _: any = Depends(get_current_active_user)):
    obj = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel no encontrada")
    return obj


@router.post("/", response_model=ParcelSchema, status_code=status.HTTP_201_CREATED)
def create_parcel(
    parcel_in: ParcelCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = Parcel(**parcel_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{parcel_id}", response_model=ParcelSchema)
def update_parcel(
    parcel_id: int,
    parcel_in: ParcelUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel no encontrada")

    data = parcel_in.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{parcel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel no encontrada")
    db.delete(obj)
    db.commit()
