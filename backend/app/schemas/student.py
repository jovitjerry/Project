from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class StudentBase(BaseModel):
    student_id: str = Field(..., description="Unique Student ID / Roll Number")
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=8)
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    profile_image: Optional[str] = None

class StudentCreate(StudentBase):
    user_id: Optional[int] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=8)
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    profile_image: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
