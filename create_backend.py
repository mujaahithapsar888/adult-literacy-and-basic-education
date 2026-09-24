import os

def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Directories
dirs = [
    "backend/app/config",
    "backend/app/database",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/routes",
    "backend/app/services",
    "backend/app/repositories",
    "backend/app/authentication",
    "backend/app/middleware",
    "backend/app/ml",
    "backend/app/dl",
    "backend/app/nlp",
    "backend/app/genai",
    "backend/app/agent",
    "backend/app/utils",
    "backend/app/logs",
    "backend/tests"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    # create __init__.py
    if d != "backend/tests" and "logs" not in d:
        create_file(os.path.join(d, "__init__.py"))

# Requirements
create_file("backend/requirements.txt", """
fastapi==0.104.1
uvicorn==0.24.0.post1
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.2
pydantic-settings==2.1.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
psycopg2-binary==2.9.9
scikit-learn==1.3.2
tensorflow==2.15.0
spacy==3.7.2
sentence-transformers==2.2.2
google-generativeai==0.3.1
langgraph==0.0.10
""")

# Config
create_file("backend/app/config/settings.py", """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduDash API"
    DATABASE_URL: str = "sqlite:///./test.db"  # Using SQLite for easy local dev, replace with Postgres for production
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
""")

# Database Connection
create_file("backend/app/database/connection.py", """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

# Models
create_file("backend/app/models/user.py", """
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="Student") # Student, Teacher, Admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    profile = relationship("StudentProfile", back_populates="user", uselist=False)

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    education_level = Column(String)
    learning_goal = Column(String)
    
    user = relationship("User", back_populates="profile")
""")

# Schemas
create_file("backend/app/schemas/user.py", """
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "Student"

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
""")

# Authentication Security
create_file("backend/app/authentication/security.py", """
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
""")

# Repositories
create_file("backend/app/repositories/user_repo.py", """
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.authentication.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
""")

# Services (Business Logic)
create_file("backend/app/services/auth_service.py", """
from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.schemas.user import UserCreate
from app.authentication.security import verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from app.config.settings import settings

def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def login_for_access_token(db: Session, form_data):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
""")

# Routes
create_file("backend/app/routes/auth.py", """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.repositories import user_repo
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repo.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login_for_access_token(db, form_data)
""")

# Placeholders for ML, DL, NLP, GenAI, Agent
create_file("backend/app/ml/recommender.py", """
# Random Forest / XGBoost based Recommendation Engine Stub
def generate_recommendations(user_id: int):
    return ["Lesson A", "Lesson B"]
""")

create_file("backend/app/genai/quiz_generator.py", """
# Google Gemini API Stub
def generate_quiz(topic: str):
    return {"questions": []}
""")

create_file("backend/app/agent/workflow.py", """
# LangGraph Workflow Stub
def run_student_workflow(user_id: int):
    pass
""")

# Main entry point
create_file("backend/app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.database.connection import Base, engine

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduDash API",
    description="Production-ready FastAPI backend for EduDash",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/")
def health_check():
    return {"status": "ok", "message": "EduDash API is running!"}

# Include Routers
app.include_router(auth.router)
""")

print("Backend scaffolded successfully!")
