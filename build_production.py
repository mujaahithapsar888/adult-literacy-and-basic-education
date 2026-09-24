import os
import subprocess

def rewrite(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def run(cmd, cwd="."):
    subprocess.run(cmd, shell=True, cwd=cwd)

# 1. Update models/user.py
with open("backend/app/models/user.py", "r", encoding="utf-8") as f:
    user_code = f.read()

if "is_verified" not in user_code:
    user_code = user_code.replace('hashed_password = Column(String)', 'hashed_password = Column(String)\n    is_verified = Column(Integer, default=1) # 1 for True, 0 for False (SQLite boolean compatibility)')
    user_code += """
class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
"""
    with open("backend/app/models/user.py", "w", encoding="utf-8") as f:
        f.write(user_code)

# 2. Add Exceptions Middleware
rewrite("backend/app/middleware/exceptions.py", """
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger(__name__)

async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please contact support."}
    )
""")

# 3. Update main.py for Lifespan and Middleware
rewrite("backend/app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import auth, students, assessment, recommendations, prediction, quiz, chat, analytics, reports
from app.database.connection import Base, engine
import app.models.user
import app.models.course
import app.models.assessment
import app.models.progress
import app.models.ai_tutor
from app.middleware.exceptions import custom_exception_handler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created.")
    yield
    logger.info("Application shutdown: Cleaning up resources...")

app = FastAPI(
    title="EduDash API",
    description="Production-ready FastAPI backend for EduDash",
    version="1.0.0",
    lifespan=lifespan
)

# Exception Handler
app.add_exception_handler(Exception, custom_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "EduDash API is running in production mode!"}

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(assessment.router)
app.include_router(recommendations.router)
app.include_router(prediction.router)
app.include_router(quiz.router)
app.include_router(chat.router)
app.include_router(analytics.router)
app.include_router(reports.router)
""")

# 4. Create Dockerfile
rewrite("backend/Dockerfile", """
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

# 5. Create docker-compose.yml
rewrite("docker-compose.yml", """
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: adminpassword
      POSTGRES_DB: edudash
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://admin:adminpassword@db:5432/edudash
      - SECRET_KEY=supersecretproductionkey123
    depends_on:
      - db

volumes:
  postgres_data:
""")

# 6. Unit Tests Setup (conftest.py and test_auth.py)
rewrite("backend/tests/__init__.py", "")

rewrite("backend/tests/conftest.py", """
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
""")

rewrite("backend/tests/test_auth.py", """
def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_user_registration(client):
    response = client.post("/auth/register", json={
        "email": "testuser@edudash.com",
        "password": "strongpassword123",
        "role": "Student"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@edudash.com"

def test_user_login(client):
    response = client.post("/auth/login", data={
        "username": "testuser@edudash.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
""")
