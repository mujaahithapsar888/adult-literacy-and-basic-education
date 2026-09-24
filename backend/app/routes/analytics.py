from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def get_analytics():
    return {"learning_hours": 120, "accuracy": 88}
