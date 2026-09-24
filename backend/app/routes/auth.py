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
