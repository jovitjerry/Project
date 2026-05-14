from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Tuple
from ..models.teacher import Teacher
from ..schemas.teacher import TeacherCreate, TeacherUpdate
from .base_service import BaseService

class TeacherService(BaseService[Teacher, TeacherCreate, TeacherUpdate]):
    def __init__(self):
        super().__init__(Teacher)

    def get_teachers(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        department: Optional[str] = None
    ) -> Tuple[List[Teacher], int]:
        query = db.query(self.model)
        
        if search:
            query = query.filter(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.teacher_id.ilike(f"%{search}%"),
                    self.model.email.ilike(f"%{search}%")
                )
            )
            
        if department and department != "All Departments":
            query = query.filter(self.model.department == department)
            
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

teacher_service = TeacherService()
