import os
import uuid
from fastapi import UploadFile, HTTPException
from ..config.config import settings

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

async def save_upload_file(upload_file: UploadFile, folder: str = "profiles") -> str:
    # Ensure folder exists
    dest_dir = os.path.join("static/uploads", folder)
    os.makedirs(dest_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    if file_extension.lower() not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG and PNG allowed.")
        
    # Check file size (approximate by reading into memory or checking file object)
    content = await upload_file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size allowed is 2MB.")
    
    new_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(dest_dir, new_filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
        
    return f"uploads/{folder}/{new_filename}"

def delete_uploaded_file(file_path: str):
    if not file_path:
        return
    full_path = os.path.join("static", file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
