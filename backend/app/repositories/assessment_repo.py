from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.models.progress import StudentProgress
from app.models.course import Course
import random # For mocking

def get_assessment(db: Session, assessment_id: int):
    # In a real app, query by ID. For now we will return a mock or create one if it doesn't exist
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        course = db.query(Course).first()
        if not course:
            course = Course(title="Mock Course", description="Mock")
            db.add(course)
            db.commit()
        assessment = Assessment(id=assessment_id, course_id=course.id, title="Mock Assessment", max_score=100)
        db.add(assessment)
        db.commit()
    return assessment

def save_progress(db: Session, user_id: int, course_id: int, score: float, passed: bool):
    status = "Completed" if passed else "In Progress"
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == user_id, 
        StudentProgress.course_id == course_id
    ).first()
    
    if progress:
        progress.score = score
        progress.status = status
    else:
        progress = StudentProgress(
            user_id=user_id,
            course_id=course_id,
            status=status,
            score=score
        )
        db.add(progress)
    db.commit()
    return progress
