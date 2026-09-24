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
