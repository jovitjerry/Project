from pydantic import BaseModel
from typing import Optional, List

class CourseBase(BaseModel):
    course_id: str
    course_name: str
    course_code: str
    credits: int
    department: str
    teacher_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    credits: Optional[int] = None
    department: Optional[str] = None
    teacher_id: Optional[int] = None

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True
