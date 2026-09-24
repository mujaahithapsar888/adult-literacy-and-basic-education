from sqlalchemy.orm import Session
from app.repositories import assessment_repo
from app.schemas.assessment import AssessmentSubmission, AssessmentResult

def grade_assessment(db: Session, user_id: int, submission: AssessmentSubmission):
    assessment = assessment_repo.get_assessment(db, submission.assessment_id)
    
    # Mock grading logic: every answer is worth 10 points for simplicity
    score = len(submission.answers) * 10.0
    if score > assessment.max_score:
        score = float(assessment.max_score)
        
    passed = score >= (assessment.max_score * 0.7) # 70% to pass
    
    # Save progress
    assessment_repo.save_progress(db, user_id, assessment.course_id, score, passed)
    
    feedback = "Excellent work!" if passed else "Keep practicing, you'll get it next time!"
    
    return AssessmentResult(
        assessment_id=assessment.id,
        score=score,
        passed=passed,
        feedback=feedback
    )
