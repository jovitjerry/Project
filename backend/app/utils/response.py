from typing import Any, Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None

def success_response(data: Any = None, message: str = "Operation successful", status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
            "error": None
        }
    )

def error_response(message: str = "An error occurred", error: Any = None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
            "error": error
        }
    )
