import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

from app.config.config import settings

def fix_admin():
    db = SessionLocal()
    try:
        admin_email = settings.ADMIN_EMAIL
        admin_password = settings.ADMIN_PASSWORD
        user = db.query(User).filter(User.email == admin_email).first()
        if user:
            print(f"Updating admin ({admin_email}) password...")
            user.hashed_password = get_password_hash(admin_password)
            db.commit()
            print("Admin password updated successfully!")
        else:
            print(f"Admin user {admin_email} not found! Creating...")
            user = User(
                email=admin_email,
                hashed_password=get_password_hash(admin_password),
                full_name="System Administrator",
                role="admin"
            )
            db.add(user)
            db.commit()
            print("Admin user created successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    fix_admin()
