from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.student import StudentCreate, StudentUpdate, StudentResponse
from ..schemas.common import PaginatedResponse
from ..services.student_service import student_service
from ..auth.auth_bearer import JWTBearer, RoleChecker, get_current_user
from ..utils.file_upload import save_upload_file
from ..utils.response import success_response, error_response
from ..models.user import User

router = APIRouter()

# Role definitions
admin_only = RoleChecker(["admin"])
admin_teacher = RoleChecker(["admin", "teacher"])
any_user = JWTBearer()

@router.get("/", response_model=PaginatedResponse[StudentResponse], dependencies=[Depends(any_user)])
def read_students(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    department: Optional[str] = None,
    semester: Optional[int] = Query(None, ge=1, le=8)
):
    items, total = student_service.get_students(
        db, skip=skip, limit=limit, search=search, department=department, semester=semester
    )
    return {
        "items": items,
        "total": total,
        "page": (skip // limit) + 1,
        "size": limit
    }

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    if student_service.get_by_student_id(db, student_in.student_id):
        raise HTTPException(status_code=400, detail="Student ID already registered")
    if student_service.get_by_email(db, student_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return student_service.create(db, obj_in=student_in)

@router.get("/by-user/{user_id}", response_model=StudentResponse, dependencies=[Depends(any_user)])
def get_student_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get student profile by user account ID"""
    from ..models.student import Student
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found for this user")
    return student

@router.get("/{student_id}", response_model=StudentResponse, dependencies=[Depends(any_user)])
def read_student(student_id: int, db: Session = Depends(get_db)):
    return student_service.get(db, id=student_id)

@router.put("/{student_id}", response_model=StudentResponse, dependencies=[Depends(admin_only)])
def update_student(student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db)):
    db_obj = student_service.get(db, id=student_id)
    return student_service.update(db, db_obj=db_obj, obj_in=student_in)

@router.delete("/{student_id}", dependencies=[Depends(admin_only)])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_service.remove(db, id=student_id)
    return {"message": "Student deleted successfully"}

@router.post("/{student_id}/profile-image", dependencies=[Depends(admin_teacher)])
async def upload_profile_image(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    student = student_service.get(db, id=student_id)
    file_path = await save_upload_file(file, folder="students")

    student_in = StudentUpdate(profile_image=file_path)
    student_service.update(db, db_obj=student, obj_in=student_in)

    return {"profile_image": file_path}
