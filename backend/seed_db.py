import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from app.utils.security import get_password_hash

def seed_db():
    print("Seeding database...")
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)

    try:
        # 1. Create Admin
        if not db.query(User).filter(User.email == "admin@college.com").first():
            admin = User(
                email="admin@college.com",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role=UserRole.ADMIN
            )
            db.add(admin)
            print("Admin created.")

        # 2. Create Courses
        courses = [
            {"course_code": "CS101", "course_name": "Data Structures", "credits": 4, "department": "Computer Science"},
            {"course_code": "EC202", "course_name": "Digital Circuits", "credits": 3, "department": "Electronics"},
            {"course_code": "MA301", "course_name": "Calculus II", "credits": 4, "department": "Mathematics"},
        ]
        for c in courses:
            if not db.query(Course).filter(Course.course_code == c["course_code"]).first():
                db.add(Course(**c))
        print("Courses created.")

        # 3. Create Teachers
        teachers = [
            {"email": "teacher@college.com", "name": "Dr. Sarah Johnson", "dept": "Computer Science"},
            {"email": "miller@college.com", "name": "Prof. David Miller", "dept": "Electronics"},
        ]
        for i, t in enumerate(teachers):
            if not db.query(User).filter(User.email == t["email"]).first():
                u = User(
                    email=t["email"],
                    hashed_password=get_password_hash("password123"),
                    full_name=t["name"],
                    role=UserRole.TEACHER
                )
                db.add(u)
                db.flush()
                teacher = Teacher(
                    user_id=u.id,
                    teacher_id="T" + str(1000 + i),
                    name=t["name"],
                    email=t["email"],
                    department=t["dept"],
                    designation="Associate Professor"
                )
                db.add(teacher)
        print("Teachers created.")

        # 4. Create Students
        students = [
            {"email": "student@college.com", "name": "John Doe", "sid": "S1001", "dept": "Computer Science", "sem": 4},
            {"email": "jane@college.com", "name": "Jane Smith", "sid": "S1002", "dept": "Electronics", "sem": 2},
        ]
        for s in students:
            if not db.query(User).filter(User.email == s["email"]).first():
                u = User(
                    email=s["email"],
                    hashed_password=get_password_hash("password123"),
                    full_name=s["name"],
                    role=UserRole.STUDENT
                )
                db.add(u)
                db.flush()
                student = Student(
                    user_id=u.id,
                    student_id=s["sid"],
                    name=s["name"],
                    email=s["email"],
                    department=s["dept"],
                    semester=s["sem"]
                )
                db.add(student)
        print("Students created.")

        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
