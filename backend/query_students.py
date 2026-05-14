import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.student import Student
from app.models.user import User

def query_students():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        print("\n" + "="*80)
        print(f"{'STUDENT ID':<15} | {'NAME':<20} | {'EMAIL':<25} | {'DEPARTMENT'}")
        print("="*80)
        for s in students:
            print(f"{s.student_id:<15} | {s.name:<20} | {s.email:<25} | {s.department}")
        print("="*80 + "\n")
    finally:
        db.close()

if __name__ == "__main__":
    query_students()
