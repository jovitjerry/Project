from pydantic import BaseModel
from typing import Optional, List

class TeacherBase(BaseModel):
    teacher_id: str
    name: str
    email: str
    subject: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    salary: Optional[float] = 0.0

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    subject: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    salary: Optional[float] = None

class Teacher(TeacherBase):
    id: int

    class Config:
        from_attributes = True
