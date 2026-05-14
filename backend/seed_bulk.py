import os
import sys
import random
from datetime import datetime, timedelta

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.attendance import Attendance
from app.models.marks import Mark
from app.utils.security import get_password_hash

def seed_bulk():
    print("Seeding Bulk Fake Data...")
    db = SessionLocal()
    
    try:
        # 1. Departments & Courses
        depts = ["Computer Science", "Mechanical Eng", "Electronics", "Information Tech", "Civil Eng"]
        course_names = {
            "Computer Science": [("CS101", "Data Structures", 4), ("CS102", "Algorithms", 4)],
            "Mechanical Eng": [("ME101", "Thermodynamics", 3), ("ME102", "Fluid Mechanics", 3)],
            "Electronics": [("EC101", "Digital Design", 3), ("EC102", "Circuit Theory", 4)],
            "Information Tech": [("IT101", "Web Dev", 3), ("IT102", "Cloud Computing", 3)],
            "Civil Eng": [("CE101", "Structural Analysis", 4), ("CE102", "Surveying", 3)]
        }
        
        db_courses = []
        for dept, courses in course_names.items():
            for code, name, credits in courses:
                c = Course(course_code=code, course_name=name, credits=credits, department=dept)
                db.add(c)
                db_courses.append(c)
        db.flush()
        print(f"Created {len(db_courses)} courses across 5 departments.")

        # 2. Faculty (7)
        faculty_data = [
            ("Dr. Alan Turing", "turing@college.com", "Computer Science", "Professor"),
            ("Dr. Marie Curie", "curie@college.com", "Electronics", "Professor"),
            ("Prof. Richard Feynman", "feynman@college.com", "Mechanical Eng", "Associate Prof"),
            ("Dr. Ada Lovelace", "ada@college.com", "Information Tech", "Assistant Prof"),
            ("Prof. Isaac Newton", "newton@college.com", "Civil Eng", "Associate Prof"),
            ("Dr. Grace Hopper", "hopper@college.com", "Computer Science", "Assistant Prof"),
            ("Prof. Nikola Tesla", "tesla@college.com", "Electronics", "Senior Lecturer")
        ]
        
        db_teachers = []
        for name, email, dept, desig in faculty_data:
            u = User(email=email, hashed_password=get_password_hash("password123"), full_name=name, role=UserRole.TEACHER)
            db.add(u)
            db.flush()
            t = Teacher(user_id=u.id, teacher_id=f"T{random.randint(1000, 9999)}", name=name, email=email, department=dept, designation=desig)
            db.add(t)
            db_teachers.append(t)
        print(f"Created 7 faculty members.")

        # 3. Students (20)
        first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        db_students = []
        for i in range(20):
            fname = first_names[i]
            lname = random.choice(last_names)
            name = f"{fname} {lname}"
            email = f"{fname.lower()}.{lname.lower()}{i}@college.com"
            dept = random.choice(depts)
            
            u = User(email=email, hashed_password=get_password_hash("password123"), full_name=name, role=UserRole.STUDENT)
            db.add(u)
            db.flush()
            
            s = Student(
                user_id=u.id,
                student_id=f"S{1000+i}",
                name=name,
                email=email,
                department=dept,
                semester=random.randint(1, 8),
                phone=f"98765{i}4321",
                address=f"{i*10} College Road, Campus"
            )
            db.add(s)
            db_students.append(s)
        print(f"Created 20 students.")

        # 4. Assign Teachers to Courses
        for i, course in enumerate(db_courses):
            dept_teachers = [t for t in db_teachers if t.department == course.department]
            course.teacher_id = random.choice(dept_teachers).id if dept_teachers else random.choice(db_teachers).id
        
        # 5. Seed Attendance & Marks (Randomized)
        today = datetime.now()
        for student in db_students:
            enrolled_courses = random.sample(db_courses, 3)
            for course in enrolled_courses:
                for d in range(15):
                    date = today - timedelta(days=d)
                    status = random.choice([True, True, True, False])
                    att = Attendance(student_id=student.id, course_id=course.id, date=date.date(), status=status)
                    db.add(att)
                
                m = Mark(
                    student_id=student.id,
                    course_id=course.id,
                    marks_obtained=random.randint(40, 95),
                    total_marks=100
                )
                db.add(m)
        
        db.commit()
        print("Seeding of Attendance and Marks completed.")
        print("\nDatabase successfully seeded with 20 students, 7 faculty, 10 courses and performance data.")

    except Exception as e:
        print(f"Error seeding bulk data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_bulk()
