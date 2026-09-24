from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.assessment import AssessmentSubmission, AssessmentResult
from app.services import assessment_service
from app.authentication.security import get_current_user

router = APIRouter(prefix="/assessment", tags=["Assessment"])

@router.post("/start")
def start_assessment(category: str, difficulty: str, current_user = Depends(get_current_user)):
    # This would generate or fetch an assessment based on criteria
    return {"status": "started", "assessment_id": 101, "message": f"Started {difficulty} {category} assessment."}

@router.post("/submit", response_model=AssessmentResult)
def submit_assessment(submission: AssessmentSubmission, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return assessment_service.grade_assessment(db, current_user.id, submission)

@router.get("/result/{assessment_id}", response_model=AssessmentResult)
def get_result(assessment_id: int, current_user = Depends(get_current_user)):
    # Mock return, normally query from progress or a results table
    return AssessmentResult(assessment_id=assessment_id, score=85.0, passed=True, feedback="Good job")
