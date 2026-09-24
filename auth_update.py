import os

def rewrite(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Update Models
rewrite("backend/app/models/user.py", """
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

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
""")

# 2. Update Schemas
rewrite("backend/app/schemas/user.py", """
from pydantic import BaseModel, EmailStr

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
    refresh_token: str
    token_type: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str
""")

# 3. Update Security
rewrite("backend/app/authentication/security.py", """
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.config.settings import settings
import app.models.user as models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict):
    # Refresh tokens last longer, e.g., 7 days
    return create_token(data, timedelta(days=7))

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if blacklisted
    is_blacklisted = db.query(models.BlacklistedToken).filter(models.BlacklistedToken.token == token).first()
    if is_blacklisted:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: str):
    def role_dependency(current_user: models.User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "Admin": # Admin can access everything
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return role_dependency
""")

# 4. Update Repo
rewrite("backend/app/repositories/user_repo.py", """
from sqlalchemy.orm import Session
from app.models.user import User, BlacklistedToken, PasswordResetToken
from app.schemas.user import UserCreate
from app.authentication.security import get_password_hash
import uuid
from datetime import datetime, timedelta

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def blacklist_token(db: Session, token: str):
    bt = BlacklistedToken(token=token)
    db.add(bt)
    db.commit()

def create_reset_token(db: Session, user_id: int):
    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=1)
    prt = PasswordResetToken(user_id=user_id, token=token, expires_at=expires)
    db.add(prt)
    db.commit()
    return token

def get_reset_token(db: Session, token: str):
    return db.query(PasswordResetToken).filter(PasswordResetToken.token == token, PasswordResetToken.expires_at > datetime.utcnow()).first()

def update_password(db: Session, user: User, new_password: str):
    user.hashed_password = get_password_hash(new_password)
    db.commit()
""")

# 5. Update Auth Service
rewrite("backend/app/services/auth_service.py", """
from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.authentication.security import verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.config.settings import settings

def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
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
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def refresh_tokens(db: Session, refresh_token: str):
    credentials_exception = HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = user_repo.get_user_by_email(db, email)
    if not user:
        raise credentials_exception
        
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    new_refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

def forgot_password(db: Session, email: str):
    user = user_repo.get_user_by_email(db, email)
    if user:
        token = user_repo.create_reset_token(db, user.id)
        # In a real app, send email here. We just return it for testing.
        return {"msg": "Password reset email sent", "reset_token": token}
    return {"msg": "If email exists, a reset link was sent"}

def reset_password(db: Session, token: str, new_password: str):
    reset_record = user_repo.get_reset_token(db, token)
    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
    user = user_repo.get_user_by_id(db, reset_record.user_id)
    user_repo.update_password(db, user, new_password)
    
    # Invalidate token by deleting it (or leave it to expire)
    db.delete(reset_record)
    db.commit()
    return {"msg": "Password reset successful"}
""")

# 6. Update Auth Routes
rewrite("backend/app/routes/auth.py", """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse, Token, ForgotPassword, ResetPassword
from app.repositories import user_repo
from app.services import auth_service
from app.authentication.security import get_current_user, oauth2_scheme
from pydantic import BaseModel

class RefreshRequest(BaseModel):
    refresh_token: str

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

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_tokens(db, request.refresh_token)

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_repo.blacklist_token(db, token)
    return {"msg": "Successfully logged out"}

@router.post("/forgot-password")
def forgot_password(req: ForgotPassword, db: Session = Depends(get_db)):
    return auth_service.forgot_password(db, req.email)

@router.post("/reset-password")
def reset_password(req: ResetPassword, db: Session = Depends(get_db)):
    return auth_service.reset_password(db, req.token, req.new_password)

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user = Depends(get_current_user)):
    return current_user
""")
