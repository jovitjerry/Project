from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.utils.security import get_password_hash
from app.config.config import settings

def create_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    admin_email = settings.ADMIN_EMAIL
    admin_user = db.query(User).filter(User.email == admin_email).first()
    
    if not admin_user:
        admin_user = User(
            email=admin_email,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name="System Administrator",
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user created: {admin_email}")
    else:
        print("Admin user already exists")
    
    # Seed Students if empty
    from app.models.student import Student
    if db.query(Student).count() == 0:
        students = [
            Student(student_id="S101", name="Alice Johnson", email="alice@college.com", department="Computer Science", semester=3),
            Student(student_id="S102", name="Bob Smith", email="bob@college.com", department="Mechanical Engineering", semester=5),
            Student(student_id="S103", name="Charlie Brown", email="charlie@college.com", department="Information Technology", semester=1),
        ]
        db.add_all(students)
        print("Seeded students")

    # Seed Teachers if empty
    from app.models.teacher import Teacher
    if db.query(Teacher).count() == 0:
        teachers = [
            Teacher(teacher_id="T201", name="Dr. Sarah Lee", email="sarah@college.com", department="Computer Science", designation="Assistant Professor"),
            Teacher(teacher_id="T202", name="Prof. Mike Ross", email="mike@college.com", department="Mathematics", designation="Senior Lecturer"),
        ]
        db.add_all(teachers)
        print("Seeded teachers")

    # Seed Courses if empty
    from app.models.course import Course
    if db.query(Course).count() == 0:
        courses = [
            Course(course_id="C301", course_name="Data Structures", course_code="CS201", credits=4, department="Computer Science"),
            Course(course_id="C302", course_name="Algorithms", course_code="CS301", credits=3, department="Computer Science"),
            Course(course_id="C303", course_name="Database Systems", course_code="CS401", credits=4, department="Computer Science"),
        ]
        db.add_all(courses)
        print("Seeded courses")

    db.commit()
    db.close()

if __name__ == "__main__":
    create_admin()
