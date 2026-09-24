from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["AI Tutor"])

@router.post("/")
def chat_with_tutor(message: str):
    return {"reply": f"AI Tutor says: I can help you with {message}!"}
