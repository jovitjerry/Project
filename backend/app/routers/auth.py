from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserRole
from ..models.student import Student
from ..models.teacher import Teacher
from ..schemas.user import UserCreate, UserLogin, Token, UserResponse
from ..utils.security import get_password_hash, verify_password
from ..auth.auth_handler import signJWT, verify_refresh_token
from ..auth.auth_bearer import get_current_user
from ..utils.response import success_response, error_response

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        return error_response(message="Email already registered", status_code=400)
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if not db_user or not verify_password(user_in.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Get associated ID based on role
    profile_id = db_user.id
    if db_user.role == UserRole.STUDENT:
        student = db.query(Student).filter(Student.user_id == db_user.id).first()
        if student: profile_id = student.id
    elif db_user.role == UserRole.TEACHER:
        teacher = db.query(Teacher).filter(Teacher.user_id == db_user.id).first()
        if teacher: profile_id = teacher.id
    
    tokens = signJWT(str(db_user.id), db_user.role)
    return success_response(data={
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "token_type": "bearer",
        "role": db_user.role,
        "userId": db_user.id,        # Always the auth user account ID
        "profileId": profile_id,     # Student/teacher profile record ID
        "email": db_user.email,
        "full_name": db_user.full_name
    }, message="Login successful")


@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    tokens = signJWT(str(user.id), user.role)
    return success_response(data=tokens, message="Token refreshed")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
