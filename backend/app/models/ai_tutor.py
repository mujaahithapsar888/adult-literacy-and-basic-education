from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from app.database.connection import Base

class AITutorHistory(Base):
    __tablename__ = "ai_tutor_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, nullable=False) # user or assistant
    message_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
