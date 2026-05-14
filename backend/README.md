# College Management System - Backend

This is the FastAPI backend for the College Management System.

## Features
- JWT Authentication
- Student Management (CRUD)
- Teacher Management (CRUD - Placeholder)
- Course Management (Placeholder)
- SQLite Database with SQLAlchemy ORM
- Pydantic schemas for validation

## Setup Instructions

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize Database**:
   ```bash
   python init_db.py
   ```

6. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Default Admin Credentials
- **Email**: admin@college.edu
- **Password**: admin123
