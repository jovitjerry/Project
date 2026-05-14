from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.teacher import TeacherCreate, TeacherUpdate, Teacher as TeacherResponse
from ..schemas.common import PaginatedResponse
from ..services.teacher_service import teacher_service
from ..auth.auth_bearer import JWTBearer, RoleChecker
from ..utils.response import success_response, error_response

router = APIRouter()

# Role definitions
admin_only = RoleChecker(["admin"])
any_user = JWTBearer()

@router.get("/", response_model=PaginatedResponse[TeacherResponse], dependencies=[Depends(any_user)])
def read_teachers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    department: Optional[str] = None
):
    items, total = teacher_service.get_teachers(
        db, skip=skip, limit=limit, search=search, department=department
    )
    return {
        "items": items,
        "total": total,
        "page": (skip // limit) + 1,
        "size": limit
    }

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
def create_teacher(teacher_in: TeacherCreate, db: Session = Depends(get_db)):
    # Check if teacher_id or email exists
    # (Assuming teacher_id is unique)
    return teacher_service.create(db, obj_in=teacher_in)

@router.get("/{teacher_id}", response_model=TeacherResponse, dependencies=[Depends(any_user)])
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return teacher_service.get(db, id=teacher_id)

@router.put("/{teacher_id}", response_model=TeacherResponse, dependencies=[Depends(admin_only)])
def update_teacher(teacher_id: int, teacher_in: TeacherUpdate, db: Session = Depends(get_db)):
    db_obj = teacher_service.get(db, id=teacher_id)
    return teacher_service.update(db, db_obj=db_obj, obj_in=teacher_in)

@router.delete("/{teacher_id}", dependencies=[Depends(admin_only)])
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher_service.remove(db, id=teacher_id)
    return {"message": "Teacher deleted successfully"}
