from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.course import Course
from ..schemas.course import CourseCreate, CourseUpdate, Course as CourseSchema
from ..auth.auth_bearer import JWTBearer

router = APIRouter()

@router.get("/", response_model=List[CourseSchema], dependencies=[Depends(JWTBearer())])
def get_courses(
    skip: int = 0, 
    limit: int = 100, 
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    if department and department != "All Departments":
        query = query.filter(Course.department == department)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=CourseSchema, dependencies=[Depends(JWTBearer())])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/{course_id}", response_model=CourseSchema, dependencies=[Depends(JWTBearer())])
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.put("/{course_id}", response_model=CourseSchema, dependencies=[Depends(JWTBearer())])
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/{course_id}", dependencies=[Depends(JWTBearer())])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}
