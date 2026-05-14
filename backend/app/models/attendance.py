from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Attendance(Base, TimestampMixin):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    date = Column(String) # Storing as string YYYY-MM-DD
    status = Column(Boolean, default=False) # True for Present, False for Absent

    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")
