from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from app.database.connection import Base

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String, nullable=False)
    max_score = Column(Integer, default=100)

class Quiz(Base):
    # Generative AI output storage
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    topic = Column(String, nullable=False)
    questions_json = Column(Text, nullable=False) # Stores Gemini JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
