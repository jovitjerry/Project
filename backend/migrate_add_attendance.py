import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(students)"))
        columns = [row[1] for row in result.fetchall()]

        if 'attendance_percentage' not in columns:
            conn.execute(text("ALTER TABLE students ADD COLUMN attendance_percentage REAL"))
            conn.commit()
            print("[OK] Column 'attendance_percentage' added to students table.")
        else:
            print("[OK] Column 'attendance_percentage' already exists.")

        # Populate cgpa
        conn.execute(text("""
            UPDATE students
            SET cgpa = ROUND((5 + (ABS(RANDOM()) % 50) / 10.0), 2)
            WHERE cgpa IS NULL OR cgpa = 0;
        """))
        # Populate attendance_percentage
        conn.execute(text("""
            UPDATE students
            SET attendance_percentage = ROUND((60 + (ABS(RANDOM()) % 40) + (ABS(RANDOM()) % 10) / 10.0), 1)
            WHERE attendance_percentage IS NULL OR attendance_percentage = 0;
        """))
        conn.commit()
        print("[OK] Populated cgpa and attendance_percentage values for students.")

if __name__ == "__main__":
    migrate()
