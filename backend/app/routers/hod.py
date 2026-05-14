import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.student import Student
from ..models.teacher import Teacher
from ..models.course import Course
from ..models.attendance import Attendance
from ..models.marks import Mark
from ..models.hod_models import Timetable, Grievance, Notice
from ..schemas.hod_schemas import GrievanceUpdate, NoticeCreate, NoticeUpdate
from ..auth.auth_bearer import JWTBearer, get_current_user
from ..utils.response import success_response, error_response

router = APIRouter()

TIMETABLES_DIR = "static/timetables"
os.makedirs(TIMETABLES_DIR, exist_ok=True)


def get_hod_department(current_user: User = Depends(get_current_user)) -> str:
    """Extract and validate the HOD's department from their user record."""
    if current_user.role not in (UserRole.HOD, UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to HOD users"
        )
    if not current_user.department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="HOD account has no department assigned. Contact admin."
        )
    return current_user.department


@router.get("/stats", dependencies=[Depends(JWTBearer())])
def get_hod_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)

    total_students = db.query(Student).filter(Student.department == dept).count()
    total_teachers = db.query(Teacher).filter(Teacher.department == dept).count()
    total_courses = db.query(Course).filter(Course.department == dept).count()

    # Attendance
    students_with_att = db.query(Student.attendance_percentage).filter(Student.department == dept, Student.attendance_percentage.isnot(None)).all()
    att_values = [s[0] for s in students_with_att if s[0] > 0]
    attendance_percentage = (sum(att_values) / len(att_values)) if att_values else 0

    semester_stats = db.query(
        Student.semester,
        func.count(Student.id)
    ).filter(Student.department == dept).group_by(Student.semester).all()

    dept_student_ids = [s.id for s in db.query(Student.id).filter(Student.department == dept).all()]

    # Pass percentage proxy: percentage of marks above 40
    if dept_student_ids:
        all_marks = db.query(Mark).filter(Mark.student_id.in_(dept_student_ids)).all()
        total_marks = len(all_marks)
        pass_marks = sum(1 for m in all_marks if m.marks_obtained >= 40)
        pass_percentage = (pass_marks / total_marks * 100) if total_marks > 0 else 0
        
        # Calculate avg_cgpa
        students_with_cgpa = db.query(Student.cgpa).filter(Student.department == dept, Student.cgpa.isnot(None)).all()
        cgpa_values = [s[0] for s in students_with_cgpa if s[0] > 0]
        avg_cgpa = (sum(cgpa_values) / len(cgpa_values)) if cgpa_values else 0
    else:
        pass_percentage = 0
        avg_cgpa = 0

    data = {
        "department": dept,
        "hod_name": current_user.full_name,
        "total_students": total_students,
        "total_faculty": total_teachers,
        "total_courses": total_courses,
        "attendance_percentage": round(attendance_percentage, 2),
        "pass_percentage": round(pass_percentage, 2),
        "avg_cgpa": round(avg_cgpa, 2),
        "semester_distribution": {f"Sem {sem}": count for sem, count in semester_stats if sem}
    }
    return success_response(data=data, message="HOD dashboard stats retrieved successfully")


@router.get("/faculty", dependencies=[Depends(JWTBearer())])
def get_hod_faculty(
    search: str = "",
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)

    query = db.query(Teacher).filter(Teacher.department == dept)
    if search:
        query = query.filter(or_(
            Teacher.name.ilike(f"%{search}%"),
            Teacher.email.ilike(f"%{search}%"),
            Teacher.teacher_id.ilike(f"%{search}%")
        ))
    
    total = query.count()
    teachers = query.offset(skip).limit(limit).all()

    data = {
        "total": total,
        "items": [
            {
                "id": t.id,
                "teacher_id": t.teacher_id,
                "name": t.name,
                "email": t.email,
                "designation": t.designation,
                "subject": t.subject,
                "phone": t.phone,
                "department": t.department
            }
            for t in teachers
        ]
    }
    return success_response(data=data, message=f"Faculty for {dept} retrieved")


@router.get("/students", dependencies=[Depends(JWTBearer())])
def get_hod_students(
    search: str = "",
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)

    query = db.query(Student).filter(Student.department == dept)
    if search:
        query = query.filter(or_(
            Student.name.ilike(f"%{search}%"),
            Student.email.ilike(f"%{search}%"),
            Student.student_id.ilike(f"%{search}%")
        ))
    
    total = query.count()
    students = query.offset(skip).limit(limit).all()

    data = {
        "total": total,
        "items": []
    }
    
    for s in students:
        data["items"].append({
            "id": s.id,
            "student_id": s.student_id,
            "name": s.name,
            "email": s.email,
            "semester": s.semester,
            "department": s.department,
            "cgpa": s.cgpa or 0,
            "attendance_percentage": s.attendance_percentage or 0
        })
    return success_response(data=data, message=f"Students for {dept} retrieved")


@router.get("/performance", dependencies=[Depends(JWTBearer())])
def get_hod_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)

    # CGPA Analytics
    students = db.query(Student).filter(Student.department == dept, Student.cgpa.isnot(None), Student.cgpa > 0).all()
    cgpas = [s.cgpa for s in students]
    
    avg_cgpa = sum(cgpas) / len(cgpas) if cgpas else 0
    highest_cgpa = max(cgpas) if cgpas else 0
    lowest_cgpa = min(cgpas) if cgpas else 0

    top_students = sorted(students, key=lambda x: x.cgpa, reverse=True)[:5]
    low_students = [s for s in students if s.cgpa < 6.0 or (s.attendance_percentage and s.attendance_percentage < 75.0)] 

    top_students_data = [{"id": s.id, "name": s.name, "student_id": s.student_id, "cgpa": s.cgpa, "attendance_percentage": s.attendance_percentage or 0} for s in top_students]
    low_students_data = [{"id": s.id, "name": s.name, "student_id": s.student_id, "cgpa": s.cgpa, "attendance_percentage": s.attendance_percentage or 0} for s in low_students]

    data = {
        "cgpa_stats": {
            "avg_cgpa": round(avg_cgpa, 2),
            "highest_cgpa": highest_cgpa,
            "lowest_cgpa": lowest_cgpa
        },
        "top_students": top_students_data,
        "low_students": low_students_data
    }
    return success_response(data=data, message=f"Performance for {dept} retrieved")


# --- Timetable Management ---

@router.post("/timetable", dependencies=[Depends(JWTBearer())])
async def upload_timetable(
    semester: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    
    # Save file
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(TIMETABLES_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Check if timetable for this semester already exists, if so delete old file
    existing = db.query(Timetable).filter(Timetable.department == dept, Timetable.semester == semester).first()
    if existing:
        if os.path.exists(existing.file_path):
            os.remove(existing.file_path)
        existing.file_path = file_path
        existing.original_filename = file.filename
        db.commit()
        db.refresh(existing)
        return success_response(data={"id": existing.id, "file_path": file_path}, message="Timetable updated successfully")
    
    new_timetable = Timetable(
        department=dept,
        semester=semester,
        file_path=file_path,
        original_filename=file.filename
    )
    db.add(new_timetable)
    db.commit()
    db.refresh(new_timetable)
    
    return success_response(data={"id": new_timetable.id, "file_path": file_path}, message="Timetable uploaded successfully")


@router.get("/timetable", dependencies=[Depends(JWTBearer())])
def get_timetables(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Both students and faculty might need this, but for now we secure it by HOD's dept.
    # To make it accessible to students/faculty of the same dept, we'd adjust the auth logic.
    # For HOD:
    dept = get_hod_department(current_user)
    timetables = db.query(Timetable).filter(Timetable.department == dept).all()
    
    data = [
        {
            "id": t.id,
            "semester": t.semester,
            "original_filename": t.original_filename,
            "file_url": f"/{t.file_path}",
            "created_at": t.created_at
        }
        for t in timetables
    ]
    return success_response(data=data, message="Timetables retrieved successfully")


@router.delete("/timetable/{timetable_id}", dependencies=[Depends(JWTBearer())])
def delete_timetable(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id, Timetable.department == dept).first()
    
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
        
    if os.path.exists(timetable.file_path):
        os.remove(timetable.file_path)
        
    db.delete(timetable)
    db.commit()
    return success_response(message="Timetable deleted successfully")


# --- Grievances Management ---

@router.get("/grievances", dependencies=[Depends(JWTBearer())])
def get_grievances(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    query = db.query(Grievance).filter(Grievance.department == dept)
    
    if status:
        query = query.filter(Grievance.status == status)
        
    grievances = query.order_by(Grievance.created_at.desc()).all()
    data = [
        {
            "id": g.id,
            "title": g.title,
            "description": g.description,
            "status": g.status,
            "submitted_by": g.submitted_by,
            "submitter_type": g.submitter_type,
            "created_at": g.created_at
        }
        for g in grievances
    ]
    return success_response(data=data, message="Grievances retrieved successfully")


@router.put("/grievances/{grievance_id}", dependencies=[Depends(JWTBearer())])
def update_grievance_status(
    grievance_id: int,
    update_data: GrievanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id, Grievance.department == dept).first()
    
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
        
    grievance.status = update_data.status
    db.commit()
    db.refresh(grievance)
    return success_response(message="Grievance status updated")


# --- Notices Management ---

@router.get("/notices", dependencies=[Depends(JWTBearer())])
def get_notices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    notices = db.query(Notice).filter(Notice.department == dept).order_by(Notice.date.desc()).all()
    
    data = [
        {
            "id": n.id,
            "title": n.title,
            "description": n.description,
            "date": n.date,
            "created_at": n.created_at
        }
        for n in notices
    ]
    return success_response(data=data, message="Notices retrieved successfully")


@router.post("/notices", dependencies=[Depends(JWTBearer())])
def create_notice(
    notice_data: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    new_notice = Notice(
        title=notice_data.title,
        description=notice_data.description,
        date=notice_data.date,
        department=dept
    )
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return success_response(message="Notice created successfully")


@router.put("/notices/{notice_id}", dependencies=[Depends(JWTBearer())])
def update_notice(
    notice_id: int,
    notice_data: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    notice = db.query(Notice).filter(Notice.id == notice_id, Notice.department == dept).first()
    
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    if notice_data.title: notice.title = notice_data.title
    if notice_data.description: notice.description = notice_data.description
    if notice_data.date: notice.date = notice_data.date
    
    db.commit()
    db.refresh(notice)
    return success_response(message="Notice updated successfully")


@router.delete("/notices/{notice_id}", dependencies=[Depends(JWTBearer())])
def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = get_hod_department(current_user)
    notice = db.query(Notice).filter(Notice.id == notice_id, Notice.department == dept).first()
    
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    db.delete(notice)
    db.commit()
    return success_response(message="Notice deleted successfully")
