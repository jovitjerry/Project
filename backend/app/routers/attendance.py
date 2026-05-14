from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.attendance import Attendance
from ..models.student import Student
from ..models.course import Course
from ..schemas.attendance import AttendanceCreate, Attendance as AttendanceSchema, AttendanceReport
from ..auth.auth_bearer import JWTBearer

router = APIRouter()

@router.post("/", response_model=AttendanceSchema, dependencies=[Depends(JWTBearer())])
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.course_id == attendance.course_id,
        Attendance.date == attendance.date
    ).first()

    if existing:
        existing.status = attendance.status
        db.commit()
        db.refresh(existing)
        return existing

    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.post("/bulk", dependencies=[Depends(JWTBearer())])
def mark_attendance_bulk(attendance_list: List[AttendanceCreate], db: Session = Depends(get_db)):
    for attendance in attendance_list:
        existing = db.query(Attendance).filter(
            Attendance.student_id == attendance.student_id,
            Attendance.course_id == attendance.course_id,
            Attendance.date == attendance.date
        ).first()

        if existing:
            existing.status = attendance.status
        else:
            db_attendance = Attendance(**attendance.dict())
            db.add(db_attendance)

    db.commit()
    return {"message": f"Attendance marked for {len(attendance_list)} students"}

@router.get("/student/{student_id}", response_model=List[AttendanceSchema], dependencies=[Depends(JWTBearer())])
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()

@router.get("/course/{course_id}", response_model=List[AttendanceSchema], dependencies=[Depends(JWTBearer())])
def get_course_attendance(course_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.course_id == course_id).all()

@router.get("/report/student/{student_id}", response_model=List[AttendanceReport], dependencies=[Depends(JWTBearer())])
def get_student_attendance_report(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # SQLite-compatible: fetch all attendance records per course for this student
    courses = db.query(Course).all()
    report = []

    for course in courses:
        records = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.course_id == course.id
        ).all()

        if not records:
            continue

        total = len(records)
        present = sum(1 for r in records if r.status)
        percentage = (present / total * 100) if total > 0 else 0

        report.append({
            "student_name": student.name,
            "course_name": course.course_name,
            "total_classes": total,
            "present_count": present,
            "attendance_percentage": round(percentage, 2)
        })

    return report
