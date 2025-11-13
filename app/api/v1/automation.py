from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.automation_rule import AutomationRule as AutomationRuleModel
from app.models.automation_log import AutomationLog as AutomationLogModel
from app.schemas.automation_rule import (
    AutomationRule as AutomationRuleSchema,
    AutomationRuleCreate,
    AutomationRuleUpdate,
)
from app.schemas.automation_log import (
    AutomationLog as AutomationLogSchema,
    AutomationLogCreate,
    AutomationLogUpdate,
)

router = APIRouter(
    prefix="/automation",
    tags=["automation"],
)

# =======================
# REGLAS
# =======================


@router.get("/rules", response_model=List[AutomationRuleSchema])
def list_rules(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    return db.query(AutomationRuleModel).order_by(AutomationRuleModel.priority.asc()).all()


@router.get("/rules/{rule_id}", response_model=AutomationRuleSchema)
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AutomationRuleModel).filter(AutomationRuleModel.id == rule_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla no encontrada",
        )
    return obj


@router.post("/rules", response_model=AutomationRuleSchema, status_code=status.HTTP_201_CREATED)
def create_rule(
    rule_in: AutomationRuleCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = AutomationRuleModel(**rule_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/rules/{rule_id}", response_model=AutomationRuleSchema)
def update_rule(
    rule_id: int,
    rule_in: AutomationRuleUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AutomationRuleModel).filter(AutomationRuleModel.id == rule_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla no encontrada",
        )

    data = rule_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AutomationRuleModel).filter(AutomationRuleModel.id == rule_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regla no encontrada",
        )

    db.delete(obj)
    db.commit()


# =======================
# LOGS
# =======================


@router.get("/logs", response_model=List[AutomationLogSchema])
def list_logs(
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
    limit: int = 100,
):
    q = (
        db.query(AutomationLogModel)
        .order_by(AutomationLogModel.created_at.desc())
        .limit(limit)
    )
    return q.all()


@router.get("/logs/{log_id}", response_model=AutomationLogSchema)
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AutomationLogModel).filter(AutomationLogModel.id == log_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log no encontrado",
        )
    return obj


@router.post("/logs", response_model=AutomationLogSchema, status_code=status.HTTP_201_CREATED)
def create_log(
    log_in: AutomationLogCreate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = AutomationLogModel(**log_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/logs/{log_id}", response_model=AutomationLogSchema)
def update_log(
    log_id: int,
    log_in: AutomationLogUpdate,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AutomationLogModel).filter(AutomationLogModel.id == log_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log no encontrado",
        )

    data = log_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    _: any = Depends(get_current_active_user),
):
    obj = db.query(AutomationLogModel).filter(AutomationLogModel.id == log_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log no encontrado",
        )

    db.delete(obj)
    db.commit()
