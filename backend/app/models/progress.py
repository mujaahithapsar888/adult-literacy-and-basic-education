from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from datetime import datetime
from app.database.connection import Base

class StudentProgress(Base):
    __tablename__ = "student_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    status = Column(String, default="Not Started") # Not Started, In Progress, Completed
    score = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Recommendation(Base):
    # Machine Learning output storage
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommended_course_id = Column(Integer, ForeignKey("courses.id"))
    confidence_score = Column(Float)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String) # Weekly, Final
    file_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
