from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.cooperative import Cooperative as CooperativeModel
from app.schemas.cooperative import (
    Cooperative as CooperativeSchema,
    CooperativeCreate,
    CooperativeUpdate,
)

router = APIRouter(
    prefix="/cooperatives",
    tags=["cooperatives"],
)


@router.get("/", response_model=List[CooperativeSchema])
def list_cooperatives(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(CooperativeModel).all()


@router.get("/{coop_id}", response_model=CooperativeSchema)
def get_cooperative(
    coop_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(CooperativeModel).filter(CooperativeModel.id == coop_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooperativa no encontrada",
        )
    return obj


@router.post("/", response_model=CooperativeSchema, status_code=status.HTTP_201_CREATED)
def create_cooperative(
    coop_in: CooperativeCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = CooperativeModel(**coop_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{coop_id}", response_model=CooperativeSchema)
def update_cooperative(
    coop_id: int,
    coop_in: CooperativeUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(CooperativeModel).filter(CooperativeModel.id == coop_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooperativa no encontrada",
        )

    data = coop_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{coop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cooperative(
    coop_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(CooperativeModel).filter(CooperativeModel.id == coop_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooperativa no encontrada",
        )

    db.delete(obj)
    db.commit()
