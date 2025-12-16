from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import get_current_user
from app.models import User
from app.schemas import ReportStats
from app.crud import report_stats

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/stats", response_model=ReportStats)
def stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total, avg_, mn, mx = report_stats(db, user.id)
    return ReportStats(total=total, avg_result=avg_, min_result=mn, max_result=mx)
