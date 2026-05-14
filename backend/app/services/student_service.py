from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Tuple
from ..models.student import Student
from ..schemas.student import StudentCreate, StudentUpdate
from .base_service import BaseService

class StudentService(BaseService[Student, StudentCreate, StudentUpdate]):
    def __init__(self):
        super().__init__(Student)

    def get_students(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        department: Optional[str] = None,
        semester: Optional[int] = None
    ) -> Tuple[List[Student], int]:
        query = db.query(self.model)
        
        if search:
            query = query.filter(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.student_id.ilike(f"%{search}%"),
                    self.model.email.ilike(f"%{search}%")
                )
            )
            
        if department:
            query = query.filter(self.model.department == department)
            
        if semester:
            query = query.filter(self.model.semester == semester)
            
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def get_by_student_id(self, db: Session, student_id: str) -> Optional[Student]:
        return db.query(self.model).filter(self.model.student_id == student_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Student]:
        return db.query(self.model).filter(self.model.email == email).first()

student_service = StudentService()
