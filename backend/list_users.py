import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.user import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"{'Email':<30} | {'Role':<10} | {'Name':<20}")
        print("-" * 65)
        for user in users:
            print(f"{user.email:<30} | {user.role:<10} | {user.full_name:<20}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
