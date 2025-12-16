from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.schemas import UserOut, ProfileUpdate, PasswordChange
from app.auth import get_current_user
from app.models import User
from app.crud import update_profile, change_password

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user

@router.put("", response_model=UserOut)
def update(payload: ProfileUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        updated = update_profile(db, user, payload.username, payload.email)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    return updated

@router.post("/change-password")
def change(payload: PasswordChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ok = change_password(db, user, payload.current_password, payload.new_password)
    if not ok:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    return {"status": "ok"}
