from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time

from .database import engine, Base
from .routers import auth, students, teachers, courses, attendance, marks, dashboard
from .config.config import settings
from .utils.logging import logger
from .utils.response import error_response

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A production-ready College Management System API",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify the Angular app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception at {request.url.path}: {exc}", exc_info=True)
    return error_response(
        message="An internal server error occurred. Please contact support.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error=str(exc) if settings.DEBUG else None
    )

# Include Routers with versioning prefix
api_v1_prefix = "/api/v1"
app.include_router(auth.router, prefix=f"{api_v1_prefix}/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix=f"{api_v1_prefix}/dashboard", tags=["Dashboard"])
app.include_router(students.router, prefix=f"{api_v1_prefix}/students", tags=["Students"])
app.include_router(teachers.router, prefix=f"{api_v1_prefix}/teachers", tags=["Teachers"])
app.include_router(courses.router, prefix=f"{api_v1_prefix}/courses", tags=["Courses"])
app.include_router(attendance.router, prefix=f"{api_v1_prefix}/attendance", tags=["Attendance"])
app.include_router(marks.router, prefix=f"{api_v1_prefix}/marks", tags=["Marks"])

@app.get("/api/v1/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": "1.0.0",
        "docs": "/docs"
    }
