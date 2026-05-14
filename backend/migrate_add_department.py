"""
migrate_add_department.py — Adds the 'department' column to the users table if missing.
Safe to run multiple times (idempotent).
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def migrate():
    with engine.connect() as conn:
        # Check existing columns
        result = conn.execute(
            __import__('sqlalchemy').text("PRAGMA table_info(users)")
        )
        columns = [row[1] for row in result.fetchall()]

        if 'department' not in columns:
            conn.execute(
                __import__('sqlalchemy').text(
                    "ALTER TABLE users ADD COLUMN department TEXT"
                )
            )
            conn.commit()
            print("[OK] Column 'department' added to users table.")
        else:
            print("[OK] Column 'department' already exists. No migration needed.")

if __name__ == "__main__":
    migrate()
