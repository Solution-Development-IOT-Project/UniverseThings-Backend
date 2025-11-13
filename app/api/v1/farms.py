from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.farm import Farm
from app.schemas.farm import Farm, FarmCreate, FarmUpdate

router = APIRouter(prefix="/farms", tags=["farms"])


@router.get("/", response_model=List[Farm])
def list_farms(db: Session = Depends(get_db), _: any = Depends(get_current_active_user)):
    return db.query(Farm).all()


@router.get("/{farm_id}", response_model=Farm)
def get_farm(farm_id: int, db: Session = Depends(get_db), _: any = Depends(get_current_active_user)):
    obj = db.query(Farm).filter(Farm.id == farm_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm no encontrada")
    return obj


@router.post("/", response_model=Farm, status_code=status.HTTP_201_CREATED)
def create_farm(
    farm_in: FarmCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = Farm(**farm_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{farm_id}", response_model=Farm)
def update_farm(
    farm_id: int,
    farm_in: FarmUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(Farm).filter(Farm.id == farm_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm no encontrada")

    data = farm_in.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(Farm).filter(Farm.id == farm_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm no encontrada")
    db.delete(obj)
    db.commit()
