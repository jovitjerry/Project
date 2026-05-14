import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        # Check existing columns
        result = conn.execute(text("PRAGMA table_info(students)"))
        columns = [row[1] for row in result.fetchall()]

        if 'cgpa' not in columns:
            conn.execute(text("ALTER TABLE students ADD COLUMN cgpa REAL"))
            conn.commit()
            print("[OK] Column 'cgpa' added to students table.")
        else:
            print("[OK] Column 'cgpa' already exists.")

        # Populate cgpa for students where it's NULL or 0
        conn.execute(text("""
            UPDATE students
            SET cgpa = ROUND((5 + (ABS(RANDOM()) % 50) / 10.0), 2)
            WHERE cgpa IS NULL OR cgpa = 0;
        """))
        conn.commit()
        print("[OK] Populated cgpa values for students.")

if __name__ == "__main__":
    migrate()
