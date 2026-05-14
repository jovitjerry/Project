from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TimetableResponse(BaseModel):
    id: int
    department: str
    semester: str
    file_path: str
    original_filename: str
    created_at: datetime

    class Config:
        from_attributes = True

class GrievanceCreate(BaseModel):
    title: str
    description: str

class GrievanceUpdate(BaseModel):
    status: str

class GrievanceResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    department: str
    submitted_by: str
    submitter_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class NoticeCreate(BaseModel):
    title: str
    description: str
    date: date

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None

class NoticeResponse(BaseModel):
    id: int
    title: str
    description: str
    department: str
    date: date
    created_at: datetime

    class Config:
        from_attributes = True
