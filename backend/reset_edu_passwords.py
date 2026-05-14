import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

def reset_passwords():
    db = SessionLocal()
    try:
        edu_users = db.query(User).filter(User.email.like("%@college.edu")).all()
        for user in edu_users:
            print(f"Resetting password for {user.email} to 'admin123'...")
            user.hashed_password = get_password_hash("admin123")
        db.commit()
        print("Done!")
    finally:
        db.close()

if __name__ == "__main__":
    reset_passwords()
