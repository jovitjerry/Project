# College Management System

This project is organized into a backend and a frontend.

## Project Structure

- `backend/`: FastAPI backend implementation.
- `frontend/`: Angular frontend implementation.
- `static/`: Shared static files (e.g., uploads).
- `docker-compose.yml`: Orchestration to run both services.

## How to Run

### Using Docker (Recommended)

```bash
docker-compose up --build
```

The frontend will be available at `http://localhost:4200` and the backend at `http://localhost:8000`.

### Manual Setup

#### Backend
1. Go to `backend/`.
2. Create a virtual environment: `python -m venv venv`.
3. Activate it and install dependencies: `pip install -r requirements.txt`.
4. Run: `uvicorn app.main:app --reload`.

#### Frontend
1. Go to `frontend/`.
2. Install dependencies: `npm install`.
3. Run: `npm start`.
