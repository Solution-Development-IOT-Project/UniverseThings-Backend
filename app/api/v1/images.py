from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.image import Image as ImageModel
from app.schemas.image import (
    Image as ImageSchema,
    ImageCreate,
    ImageUpdate,
)

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.get("/", response_model=List[ImageSchema])
def list_images(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(ImageModel).all()


@router.get("/{image_id}", response_model=ImageSchema)
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada",
        )
    return obj


@router.post("/", response_model=ImageSchema, status_code=status.HTTP_201_CREATED)
def create_image(
    image_in: ImageCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = ImageModel(**image_in.dict(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{image_id}", response_model=ImageSchema)
def update_image(
    image_id: int,
    image_in: ImageUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada",
        )

    data = image_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada",
        )

    db.delete(obj)
    db.commit()
