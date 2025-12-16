from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.schemas import UserCreate, TokenOut
from app.crud import create_user, authenticate_user
from app.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload.username, payload.email, payload.password)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    # Use user id as token subject so profile updates (username/email) don't invalidate tokens.
    token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=token)

@router.post("/token", response_model=TokenOut)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Use user id as token subject so profile updates (username/email) don't invalidate tokens.
    return TokenOut(access_token=create_access_token(subject=str(user.id)))
