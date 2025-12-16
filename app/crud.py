from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models import User, Calculation
from app.security import hash_password, verify_password
from app.calc import compute

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.scalar(select(User).where(User.username == username))

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.scalar(select(User).where(User.email == email))

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def create_user(db: Session, username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_profile(db: Session, user: User, username: Optional[str], email: Optional[str]) -> User:
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def change_password(db: Session, user: User, current_password: str, new_password: str) -> bool:
    if not verify_password(current_password, user.hashed_password):
        return False
    user.hashed_password = hash_password(new_password)
    db.add(user)
    db.commit()
    return True

def create_calculation(db: Session, user_id: int, a: float, b: float, op: str) -> Calculation:
    result = compute(op, a, b)
    calc = Calculation(user_id=user_id, a=a, b=b, op=op, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

def list_calculations(db: Session, user_id: int, limit: int = 50) -> List[Calculation]:
    stmt = select(Calculation).where(Calculation.user_id == user_id).order_by(Calculation.id.desc()).limit(limit)
    return list(db.scalars(stmt).all())

def report_stats(db: Session, user_id: int) -> Tuple[int, Optional[float], Optional[float], Optional[float]]:
    stmt = select(
        func.count(Calculation.id),
        func.avg(Calculation.result),
        func.min(Calculation.result),
        func.max(Calculation.result),
    ).where(Calculation.user_id == user_id)
    total, avg_, mn, mx = db.execute(stmt).one()
    return int(total or 0), (float(avg_) if avg_ is not None else None), (float(mn) if mn is not None else None), (float(mx) if mx is not None else None)
