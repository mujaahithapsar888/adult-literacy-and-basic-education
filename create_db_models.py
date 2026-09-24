import os

def rewrite(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Course & Lesson Models
rewrite("backend/app/models/course.py", """
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lessons = relationship("Lesson", back_populates="course")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String, nullable=False)
    content_url = Column(String) # Link to PDF or Video
    order_index = Column(Integer, default=0)
    
    course = relationship("Course", back_populates="lessons")
""")

# 2. Assessment & Quiz Models
rewrite("backend/app/models/assessment.py", """
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
""")

# 3. Progress, Recommendation, Report Models
rewrite("backend/app/models/progress.py", """
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
""")

# 4. AI Tutor History Model
rewrite("backend/app/models/ai_tutor.py", """
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
""")

# 5. Update main.py to import the models so they are created
with open("backend/app/main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

import_models = """from app.database.connection import Base, engine
import app.models.user
import app.models.course
import app.models.assessment
import app.models.progress
import app.models.ai_tutor"""

main_code = main_code.replace("from app.database.connection import Base, engine", import_models)

with open("backend/app/main.py", "w", encoding="utf-8") as f:
    f.write(main_code)
