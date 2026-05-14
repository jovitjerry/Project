"""
seed_hod.py — Seeds HOD (Head of Department) user accounts into the database.
Run with:  .\\venv\\Scripts\\python.exe seed_hod.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

# HOD accounts to create (email, full_name, department, password)
HOD_USERS = [
    {
        "email": "hodcse@college.com",
        "full_name": "Dr. Priya Sharma",
        "department": "Computer Science",
        "password": "hod@123",
    },
    {
        "email": "hodece@college.com",
        "full_name": "Dr. Ramesh Kumar",
        "department": "Electronics",
        "password": "hod@123",
    },
    {
        "email": "hodmech@college.com",
        "full_name": "Dr. Anil Verma",
        "department": "Mechanical Engineering",
        "password": "hod@123",
    },
    {
        "email": "hodedu@college.edu",
        "full_name": "Dr. Sarah Connor",
        "department": "Engineering",
        "password": "hod@123",
    },
]


def seed_hod_users():
    # Ensure the department column exists (non-destructive alter via SQLAlchemy)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        created = 0
        for hod in HOD_USERS:
            existing = db.query(User).filter(User.email == hod["email"]).first()
            if existing:
                # Update role and department if needed
                existing.role = UserRole.HOD
                existing.department = hod["department"]
                print(f"[updated]  {hod['email']} → role=hod, dept={hod['department']}")
            else:
                new_user = User(
                    email=hod["email"],
                    hashed_password=get_password_hash(hod["password"]),
                    full_name=hod["full_name"],
                    role=UserRole.HOD,
                    department=hod["department"],
                    is_active=True,
                )
                db.add(new_user)
                created += 1
                print(f"[created]  {hod['email']} ({hod['full_name']}) — {hod['department']}")

        db.commit()
        print(f"\nDone. {created} HOD user(s) created.")
        print("\nLogin credentials (all HODs use the same default password):")
        print("─" * 50)
        for hod in HOD_USERS:
            print(f"  Email   : {hod['email']}")
            print(f"  Password: {hod['password']}")
            print(f"  Dept    : {hod['department']}")
            print()
    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_hod_users()
