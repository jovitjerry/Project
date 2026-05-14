from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer, cast
from ..database import get_db
from ..models.student import Student
from ..models.teacher import Teacher
from ..models.course import Course
from ..models.attendance import Attendance
from ..models.marks import Mark
from ..auth.auth_bearer import JWTBearer
from ..utils.response import success_response

router = APIRouter()

@router.get("/stats", dependencies=[Depends(JWTBearer())])
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    total_teachers = db.query(Teacher).count()
    total_courses = db.query(Course).count()

    # SQLite-compatible attendance calculation
    all_attendance = db.query(Attendance).all()
    total_att = len(all_attendance)
    present_att = sum(1 for a in all_attendance if a.status)
    attendance_percentage = (present_att / total_att * 100) if total_att > 0 else 0

    # Department-wise student distribution
    dept_stats = db.query(
        Student.department,
        func.count(Student.id)
    ).group_by(Student.department).all()

    # Course-wise performance distribution
    course_stats = db.query(
        Course.course_name,
        func.avg(Mark.marks_obtained).label("avg_marks")
    ).join(Mark, Mark.course_id == Course.id).group_by(Course.course_name).all()

    data = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "attendance_percentage": round(attendance_percentage, 2),
        "department_distribution": {dept: count for dept, count in dept_stats if dept},
        "academic_performance": {course: round(float(avg), 2) if avg else 0 for course, avg in course_stats}
    }

    return success_response(data=data, message="Dashboard stats retrieved successfully")
