from fastapi import APIRouter
from pydantic import BaseModel
from app.dl import predict_score

router = APIRouter(prefix="/prediction", tags=["Prediction"])

class PredictionRequest(BaseModel):
    raisedhands: float
    visited_resources: float
    announcements_view: float
    discussion: float

@router.post("/")
def make_prediction(request: PredictionRequest):
    # Prepare features for the DL LSTM prediction
    features = [
        request.raisedhands,
        request.visited_resources,
        request.announcements_view,
        request.discussion
    ]
    
    # Get prediction from the PyTorch LSTM model
    score = predict_score(features)
    
    return {"predicted_score": score}
