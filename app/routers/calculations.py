from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import get_current_user
from app.models import User
from app.schemas import CalculationCreate, CalculationOut
from app.crud import create_calculation, list_calculations

router = APIRouter(prefix="/api/calculations", tags=["calculations"])

@router.post("", response_model=CalculationOut, status_code=201)
def create(payload: CalculationCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        calc = create_calculation(db, user.id, payload.a, payload.b, payload.op)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return calc

@router.get("", response_model=list[CalculationOut])
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list_calculations(db, user.id, limit=50)
