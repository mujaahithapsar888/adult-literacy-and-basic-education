from pydantic import BaseModel
from typing import List, Dict, Any

class AssessmentSubmission(BaseModel):
    assessment_id: int
    answers: Dict[str, str] # e.g. {"q1": "Option A"}

class AssessmentResult(BaseModel):
    assessment_id: int
    score: float
    passed: bool
    feedback: str
