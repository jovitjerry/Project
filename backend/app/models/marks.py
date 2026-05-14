from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Mark(Base, TimestampMixin):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    marks_obtained = Column(Float)
    total_marks = Column(Float, default=100.0)
    grade = Column(String)

    student = relationship("Student", back_populates="marks")
    course = relationship("Course", back_populates="marks")
