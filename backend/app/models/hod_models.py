from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Timetable(Base, TimestampMixin):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True, nullable=False)
    semester = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)

class Grievance(Base, TimestampMixin):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="Pending") # Pending, Resolved
    department = Column(String, index=True, nullable=False)
    submitted_by = Column(String, nullable=False) # Name of student/faculty
    submitter_type = Column(String, nullable=False) # Student or Faculty

class Notice(Base, TimestampMixin):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String, index=True, nullable=False)
    date = Column(Date, nullable=False)
