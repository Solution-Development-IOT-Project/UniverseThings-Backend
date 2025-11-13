from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserSchema])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    obj_in: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    data = obj_in.dict(exclude_unset=True)
    for field, value in data.items():
        if field == "password" and value:
            from app.core.security import get_password_hash
            setattr(user, "hashed_password", get_password_hash(value))
        elif field != "password":
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
