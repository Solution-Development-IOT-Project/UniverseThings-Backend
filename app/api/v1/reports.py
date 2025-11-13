from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.report import Report as ReportModel
from app.models.user import User
from app.schemas.report import (
    Report as ReportSchema,
    ReportCreate,
    ReportUpdate,
)

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/", response_model=List[ReportSchema])
def list_reports(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return db.query(ReportModel).order_by(ReportModel.created_at.desc()).all()


@router.get("/{report_id}", response_model=ReportSchema)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    obj = db.query(ReportModel).filter(ReportModel.id == report_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )
    return obj


@router.post("/", response_model=ReportSchema, status_code=status.HTTP_201_CREATED)
def create_report(
    r_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    data = r_in.dict(exclude_unset=True)
    # Si no viene created_by_id, lo seteamos al usuario actual
    if data.get("created_by_id") is None:
        data["created_by_id"] = current_user.id

    obj = ReportModel(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{report_id}", response_model=ReportSchema)
def update_report(
    report_id: int,
    r_in: ReportUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    obj = db.query(ReportModel).filter(ReportModel.id == report_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )

    data = r_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    obj = db.query(ReportModel).filter(ReportModel.id == report_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )

    db.delete(obj)
    db.commit()
