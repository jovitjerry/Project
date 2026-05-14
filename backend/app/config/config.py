from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "College Management System"
    DATABASE_URL: str = "sqlite:///./college.db"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEBUG: bool = True
    
    # Default Admin
    ADMIN_EMAIL: str = "admin@college.com"
    ADMIN_PASSWORD: str = "admin123"
    
    # Upload Settings
    UPLOAD_DIR: str = "static/uploads/profiles"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
