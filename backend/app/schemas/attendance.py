from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AttendanceBase(BaseModel):
    student_id: int
    course_id: int
    date: str
    status: bool

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[bool] = None

class Attendance(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

class AttendanceReport(BaseModel):
    student_name: str
    course_name: str
    total_classes: int
    present_count: int
    attendance_percentage: float
