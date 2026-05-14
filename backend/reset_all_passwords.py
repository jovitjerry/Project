import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

def reset_all_passwords():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            print(f"Resetting password for {user.email} to 'admin123'...")
            user.hashed_password = get_password_hash("admin123")
        db.commit()
        print("All passwords reset to 'admin123'!")
    finally:
        db.close()

if __name__ == "__main__":
    reset_all_passwords()
