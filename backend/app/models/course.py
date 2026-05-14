from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, unique=True, index=True)
    course_name = Column(String, nullable=False)
    course_code = Column(String, unique=True, index=True)
    credits = Column(Integer)
    department = Column(String)

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    teacher = relationship("Teacher", back_populates="courses")

    attendances = relationship("Attendance", back_populates="course", cascade="all, delete-orphan")
    marks = relationship("Mark", back_populates="course", cascade="all, delete-orphan")
