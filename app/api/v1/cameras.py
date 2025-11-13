from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.camera import Camera as CameraModel
from app.models.image import Image as ImageModel
from app.schemas.camera import (
    Camera as CameraSchema,
    CameraCreate,
    CameraUpdate,
)
from app.schemas.image import Image as ImageSchema

router = APIRouter(
    prefix="/cameras",
    tags=["cameras"],
)


@router.get("/", response_model=List[CameraSchema])
def list_cameras(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(CameraModel).all()


@router.get("/{camera_id}", response_model=CameraSchema)
def get_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(CameraModel).filter(CameraModel.id == camera_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cámara no encontrada",
        )
    return obj


@router.post("/", response_model=CameraSchema, status_code=status.HTTP_201_CREATED)
def create_camera(
    camera_in: CameraCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = CameraModel(**camera_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{camera_id}", response_model=CameraSchema)
def update_camera(
    camera_id: int,
    camera_in: CameraUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(CameraModel).filter(CameraModel.id == camera_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cámara no encontrada",
        )

    data = camera_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(CameraModel).filter(CameraModel.id == camera_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cámara no encontrada",
        )

    db.delete(obj)
    db.commit()


# -----------------------
# IMÁGENES DE UNA CÁMARA
# -----------------------
@router.get("/{camera_id}/images", response_model=List[ImageSchema])
def list_camera_images(
    camera_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    camera = db.query(CameraModel).filter(CameraModel.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cámara no encontrada",
        )

    q = (
        db.query(ImageModel)
        .filter(ImageModel.camera_id == camera_id)
        .order_by(ImageModel.captured_at.desc())
        .limit(limit)
    )
    return q.all()
