import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import verify_password

def test_login():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@college.com").first()
        if user:
            print(f"User found: {user.email}")
            print(f"Hashed password: {user.hashed_password}")
            is_valid = verify_password("admin123", user.hashed_password)
            print(f"Password valid ('admin123'): {is_valid}")
        else:
            print("User not found!")
    finally:
        db.close()

if __name__ == "__main__":
    test_login()
