from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import torch
from dl_pipeline import LearnerLSTM, MasteryTransformer
app = FastAPI(title="ML Prediction API", version="1.0.0")

# Load model
MODEL_PATH = "ml_models/best_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model from {MODEL_PATH}. Error: {e}")

# Load PyTorch Models
VOCAB_SIZE = 30
lstm_model = LearnerLSTM(vocab_size=VOCAB_SIZE, embed_dim=32, hidden_dim=64, output_dim=1)
transformer_model = MasteryTransformer(vocab_size=VOCAB_SIZE, embed_dim=32, num_heads=4, hidden_dim=64, output_dim=1)

try:
    lstm_model.load_state_dict(torch.load("ml_models/best_lstm.pt"))
    lstm_model.eval()
    print("Loaded LSTM model.")
except Exception as e:
    print(f"Warning: Could not load LSTM model. Error: {e}")

try:
    transformer_model.load_state_dict(torch.load("ml_models/best_transformer.pt"))
    transformer_model.eval()
    print("Loaded Transformer model.")
except Exception as e:
    print(f"Warning: Could not load Transformer model. Error: {e}")

class StudentData(BaseModel):
    age: int
    hours_studied: float
    previous_education: str
    engagement_score: float

class SequenceData(BaseModel):
    module_sequence: list[int]

@app.post("/api/v1/ml/predict")
def predict_success(data: StudentData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Feature engineering logic mirroring pipeline
    engagement_per_hour = data.engagement_score / (data.hours_studied + 1)
    
    # Create DataFrame for pipeline
    df = pd.DataFrame([{
        'age': data.age,
        'hours_studied': data.hours_studied,
        'previous_education': data.previous_education,
        'engagement_score': data.engagement_score,
        'engagement_per_hour': engagement_per_hour
    }])
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return {
        "success_prediction": int(prediction),
        "success_probability": float(probability),
        "status": "Will Pass" if prediction == 1 else "Needs Intervention"
    }

@app.post("/api/v1/ml/recommend")
def recommend_module(data: StudentData):
    """
    Recommendation logic based on student profile and predicted success.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    engagement_per_hour = data.engagement_score / (data.hours_studied + 1)
    df = pd.DataFrame([{
        'age': data.age,
        'hours_studied': data.hours_studied,
        'previous_education': data.previous_education,
        'engagement_score': data.engagement_score,
        'engagement_per_hour': engagement_per_hour
    }])
    
    prob = model.predict_proba(df)[0][1]
    
    recommendations = []
    if prob < 0.5:
        recommendations.append("Remedial Basics Module")
        recommendations.append("Time Management Skills")
    else:
        recommendations.append("Advanced Reading Comprehension")
        
    if data.engagement_score < 0.3:
        recommendations.append("Interactive Games Module (to boost engagement)")
        
    return {
        "recommended_modules": recommendations,
        "reasoning": f"Based on a {prob*100:.1f}% predicted success rate and engagement score."
    }

@app.post("/api/v1/dl/predict_sequence")
def predict_sequence(data: SequenceData):
    if lstm_model is None:
        raise HTTPException(status_code=500, detail="LSTM Model not loaded")
    
    seq_tensor = torch.tensor([data.module_sequence], dtype=torch.long)
    with torch.no_grad():
        prob = lstm_model(seq_tensor).item()
        
    return {
        "success_probability": prob,
        "prediction": int(prob >= 0.5),
        "model": "LSTM"
    }

@app.post("/api/v1/dl/predict_mastery")
def predict_mastery(data: SequenceData):
    if transformer_model is None:
        raise HTTPException(status_code=500, detail="Transformer Model not loaded")
    
    seq_tensor = torch.tensor([data.module_sequence], dtype=torch.long)
    with torch.no_grad():
        prob = transformer_model(seq_tensor).item()
        
    return {
        "success_probability": prob,
        "prediction": int(prob >= 0.5),
        "model": "Transformer"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
