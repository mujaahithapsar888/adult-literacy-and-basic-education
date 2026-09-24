from fastapi import APIRouter
from app.genai.quiz_generator import generate_quiz

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/generate")
def generate_new_quiz(topic: str = "Math"):
    return generate_quiz(topic)

@router.get("/history")
def quiz_history():
    return [{"quiz_id": 1, "score": 90}]
