from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)  # no max length (argon2)

class UserLogin(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)  # no max

class CalculationCreate(BaseModel):
    a: float
    b: float
    # Do NOT validate operator via regex here.
    # If we do, invalid operators become a 422 (validation error) before the
    # route runs. We want to return a clean 400 from our own logic.
    op: str

class CalculationOut(BaseModel):
    id: int
    a: float
    b: float
    op: str
    result: float

    class Config:
        from_attributes = True

class ReportStats(BaseModel):
    total: int
    avg_result: Optional[float]
    min_result: Optional[float]
    max_result: Optional[float]
