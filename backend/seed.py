import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.course import Course
from app.models.attendance import Attendance
from app.models.marks import Mark
from app.utils.security import get_password_hash
import datetime

def seed_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin exists
        if not db.query(User).filter(User.email == "admin@college.edu").first():
            print("Creating Admin User...")
            admin = User(
                email="admin@college.edu",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                full_name="System Admin",
                is_active=True
            )
            db.add(admin)
            
        if not db.query(User).filter(User.email == "teacher@college.edu").first():
            print("Creating Teacher User...")
            teacher_user = User(
                email="teacher@college.edu",
                hashed_password=get_password_hash("password123"),
                role=UserRole.TEACHER,
                full_name="John Doe",
                is_active=True
            )
            db.add(teacher_user)
            db.flush() # get id
            
            # Use timestamp to avoid UNIQUE constraint conflicts
            timestamp_str = str(int(datetime.datetime.now().timestamp()))
            
            teacher_profile = Teacher(
                teacher_id=f"T_{timestamp_str}",
                name="John Doe",
                email="teacher@college.edu",
                subject="Computer Science",
                department="Engineering",
                phone="1234567890",
                salary=60000.0,
                designation="Professor",
                user_id=teacher_user.id
            )
            db.add(teacher_profile)
            
        if not db.query(User).filter(User.email == "student@college.edu").first():
            print("Creating Student User...")
            student_user = User(
                email="student@college.edu",
                hashed_password=get_password_hash("password123"),
                role=UserRole.STUDENT,
                full_name="Jane Smith",
                is_active=True
            )
            db.add(student_user)
            db.flush()
            
            timestamp_str = str(int(datetime.datetime.now().timestamp()))
            
            student_profile = Student(
                student_id=f"S_{timestamp_str}",
                name="Jane Smith",
                email="student@college.edu",
                phone="0987654321",
                department="Engineering",
                semester=1,
                date_of_birth="2000-01-01",
                address="123 College St",
                user_id=student_user.id
            )
            db.add(student_profile)
            
        db.commit()
        
        # Add some courses
        teacher = db.query(Teacher).filter(Teacher.email == "teacher@college.edu").first()
        if not db.query(Course).first():
            print("Creating Courses...")
            course1 = Course(
                course_id="C101",
                course_name="Data Structures",
                course_code="CS101",
                credits=4,
                department="Engineering",
                teacher_id=teacher.id if teacher else None
            )
            db.add(course1)
            
            course2 = Course(
                course_id="C102",
                course_name="Algorithms",
                course_code="CS102",
                credits=4,
                department="Engineering",
                teacher_id=teacher.id if teacher else None
            )
            db.add(course2)
            db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
