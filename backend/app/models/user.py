from sqlalchemy import Column, Integer, String, Enum, Boolean
from ..database import Base
from .base import TimestampMixin
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.STUDENT)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    profile_image = Column(String, nullable=True)
