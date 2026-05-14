from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Teacher(Base, TimestampMixin):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    subject = Column(String)
    department = Column(String)
    phone = Column(String)
    salary = Column(Float)
    designation = Column(String)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User")

    courses = relationship("Course", back_populates="teacher", cascade="all, delete-orphan")
