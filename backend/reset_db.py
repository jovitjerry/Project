import os
import sys
from sqlalchemy import MetaData

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.attendance import Attendance
from app.models.marks import Mark
from app.utils.security import get_password_hash
from app.config.config import settings

def reset_database():
    print("Resetting Database...")
    
    # 1. Drop all tables
    try:
        Base.metadata.drop_all(bind=engine)
        print("All tables dropped.")
    except Exception as e:
        print(f"Could not drop tables: {e}")
            
    # 2. Recreate tables
    Base.metadata.create_all(bind=engine)
    print("Tables recreated.")

    # 3. Create fresh Admin user
    db = SessionLocal()
    try:
        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name="System Administrator",
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created: {settings.ADMIN_EMAIL}")
        print(f"Password: {settings.ADMIN_PASSWORD}")
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

    print("\nDatabase is now clean. Only the Admin account exists.")

if __name__ == "__main__":
    reset_database()
