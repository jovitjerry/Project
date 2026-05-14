from typing import Generic, Type, TypeVar, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from fastapi import HTTPException, status

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{self.model.__name__} with id {id} not found"
            )
        return obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Tuple[List[ModelType], int]:
        query = db.query(self.model)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        obj = self.get(db, id=id)
        db.delete(obj)
        db.commit()
        return obj

    def search(
        self, 
        db: Session, 
        *, 
        query_str: str, 
        search_fields: List[str], 
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[ModelType], int]:
        query = db.query(self.model)
        filters = []
        for field in search_fields:
            if hasattr(self.model, field):
                filters.append(getattr(self.model, field).ilike(f"%{query_str}%"))
        
        if filters:
            query = query.filter(or_(*filters))
            
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
