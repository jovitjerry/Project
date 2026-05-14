from pydantic import BaseModel
from typing import Optional, List

class MarkBase(BaseModel):
    student_id: int
    course_id: int
    marks_obtained: float
    total_marks: float = 100.0
    grade: Optional[str] = None

class MarkCreate(MarkBase):
    pass

class MarkUpdate(BaseModel):
    marks_obtained: Optional[float] = None
    grade: Optional[str] = None

class Mark(MarkBase):
    id: int

    class Config:
        from_attributes = True

class StudentResult(BaseModel):
    course_name: str
    marks_obtained: float
    total_marks: float
    grade: str
    gpa: float
