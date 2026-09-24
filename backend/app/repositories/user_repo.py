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
