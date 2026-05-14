from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.marks import Mark
from ..models.course import Course
from ..models.student import Student
from ..schemas.marks import MarkCreate, Mark as MarkSchema, StudentResult
from ..auth.auth_bearer import JWTBearer

router = APIRouter()

def calculate_grade(marks: float, total: float) -> str:
    percentage = (marks / total) * 100
    if percentage >= 90: return "S"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 50: return "D"
    return "F"

def calculate_gpa_point(grade: str) -> float:
    points = {"S": 10.0, "A": 9.0, "B": 8.0, "C": 7.0, "D": 6.0, "F": 0.0}
    return points.get(grade, 0.0)

@router.post("/", response_model=MarkSchema, dependencies=[Depends(JWTBearer())])
def add_marks(mark: MarkCreate, db: Session = Depends(get_db)):
    if not mark.grade:
        mark.grade = calculate_grade(mark.marks_obtained, mark.total_marks)

    existing = db.query(Mark).filter(
        Mark.student_id == mark.student_id,
        Mark.course_id == mark.course_id
    ).first()

    if existing:
        existing.marks_obtained = mark.marks_obtained
        existing.total_marks = mark.total_marks
        existing.grade = mark.grade
        db.commit()
        db.refresh(existing)
        return existing

    db_mark = Mark(**mark.dict())
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark

@router.post("/bulk", dependencies=[Depends(JWTBearer())])
def add_marks_bulk(marks: List[MarkCreate], db: Session = Depends(get_db)):
    """Upload marks for multiple students at once"""
    saved = 0
    for mark in marks:
        if mark.marks_obtained is None:
            continue
        if not mark.grade:
            mark.grade = calculate_grade(mark.marks_obtained, mark.total_marks)

        existing = db.query(Mark).filter(
            Mark.student_id == mark.student_id,
            Mark.course_id == mark.course_id
        ).first()

        if existing:
            existing.marks_obtained = mark.marks_obtained
            existing.total_marks = mark.total_marks
            existing.grade = mark.grade
        else:
            db_mark = Mark(**mark.dict())
            db.add(db_mark)
        saved += 1

    db.commit()
    return {"message": f"Marks saved for {saved} students"}

@router.get("/student/{student_id}", response_model=List[StudentResult], dependencies=[Depends(JWTBearer())])
def get_student_results(student_id: int, db: Session = Depends(get_db)):
    results = db.query(Mark, Course.course_name)\
                .join(Course, Mark.course_id == Course.id)\
                .filter(Mark.student_id == student_id).all()

    report = []
    for mark, course_name in results:
        report.append({
            "course_name": course_name,
            "marks_obtained": mark.marks_obtained,
            "total_marks": mark.total_marks,
            "grade": mark.grade,
            "gpa": calculate_gpa_point(mark.grade)
        })
    return report

@router.get("/course/{course_id}", dependencies=[Depends(JWTBearer())])
def get_course_marks(course_id: int, db: Session = Depends(get_db)):
    """Get all marks for a course"""
    results = db.query(Mark, Student.name, Student.student_id)\
                .join(Student, Mark.student_id == Student.id)\
                .filter(Mark.course_id == course_id).all()
    
    return [
        {
            "student_name": name,
            "student_roll": roll,
            "marks_obtained": mark.marks_obtained,
            "total_marks": mark.total_marks,
            "grade": mark.grade
        }
        for mark, name, roll in results
    ]
