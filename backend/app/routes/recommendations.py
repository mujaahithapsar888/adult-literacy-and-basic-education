from fastapi import APIRouter
from app.ml.recommender import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/")
def get_recommendations(user_id: int = 1):
    return generate_recommendations(user_id)
