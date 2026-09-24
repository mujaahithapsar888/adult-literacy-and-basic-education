from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import nlp_pipeline

app = FastAPI(title="NLP Analysis API", version="1.0.0")

class TextPayload(BaseModel):
    text: str
    expected_concepts: Optional[List[str]] = None

@app.post("/api/v1/nlp/analyze_essay")
def analyze_essay(payload: TextPayload):
    try:
        results = nlp_pipeline.comprehensive_analysis(payload.text, payload.expected_concepts)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/nlp/feedback")
def get_feedback(payload: TextPayload):
    try:
        clean = nlp_pipeline.clean_text(payload.text)
        grammar = nlp_pipeline.generate_grammar_feedback(clean)
        ling = nlp_pipeline.analyze_linguistics(clean)
        return {
            "grammar_feedback": grammar,
            "reading_level": ling["reading_level"],
            "reading_ease": ling["reading_ease"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/nlp/tutor_sentiment")
def analyze_tutor_conversation(payload: TextPayload):
    try:
        clean = nlp_pipeline.clean_text(payload.text)
        sentiment = nlp_pipeline.analyze_sentiment(clean)
        keywords = nlp_pipeline.extract_keywords(clean, top_n=3)
        return {
            "sentiment": sentiment,
            "main_topics": keywords
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
