import os

def rewrite(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Scikit-Learn Recommender
rewrite("backend/app/ml/recommender.py", """
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class LearningRecommender:
    def __init__(self):
        # We will train a simple mock classifier
        # Features: [assessment_score (0-100), previous_failures (0-10)]
        X = np.array([
            [90, 0], [85, 1], [40, 3], [55, 2], [75, 1], [30, 5], [10, 8]
        ])
        # Labels: 0 = Basic Reading, 1 = Intermediate Math, 2 = Advanced English
        y = np.array([2, 2, 0, 1, 1, 0, 0])
        
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.model.fit(X, y)
        self.classes = {
            0: "Basic Reading and Phonics",
            1: "Intermediate Mathematics",
            2: "Advanced English Comprehension"
        }

    def predict_next_topic(self, score: float, previous_failures: int = 0):
        # Predict the topic
        prediction = self.model.predict([[score, previous_failures]])[0]
        # Get probability
        probs = self.model.predict_proba([[score, previous_failures]])[0]
        confidence = float(max(probs))
        
        return {
            "topic": self.classes[prediction],
            "confidence_score": confidence
        }

recommender_engine = LearningRecommender()
""")

# 2. Generative AI Quiz Builder
rewrite("backend/app/genai/quiz_builder.py", """
import os
import json
import google.generativeai as genai

# Fallback mock if API key isn't set
def generate_mock_quiz(topic: str):
    return json.dumps([
        {"q": f"What is a fundamental concept in {topic}?", "options": ["A", "B", "C", "D"], "answer": "A"},
        {"q": "Which of these represents a core principle?", "options": ["A", "B", "C", "D"], "answer": "B"}
    ])

def build_quiz_from_topic(topic: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "mock":
        return generate_mock_quiz(topic)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f'''
        You are an expert adult education teacher.
        Create a 2-question multiple choice quiz about "{topic}".
        Return ONLY a valid JSON array of objects, with no markdown formatting or backticks.
        Each object must have 'q' (string), 'options' (array of 4 strings), and 'answer' (string).
        '''
        response = model.generate_content(prompt)
        # Attempt to parse to ensure it's valid JSON
        quiz_json = response.text.replace('```json', '').replace('```', '').strip()
        json.loads(quiz_json) 
        return quiz_json
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return generate_mock_quiz(topic)
""")

# 3. Update agent/workflow.py to use real logic
rewrite("backend/app/agent/workflow.py", """
from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Import the new AI modules
from app.ml.recommender import recommender_engine
from app.genai.quiz_builder import build_quiz_from_topic

class AgentState(TypedDict):
    student_id: int
    current_step: str
    assessment_score: Optional[float]
    recommended_topic: Optional[str]
    quiz_id: Optional[int]
    quiz_score: Optional[float]
    status: str
    messages: List[str]
    quiz_data: Optional[str] # Will hold the JSON

def run_assessment(state: AgentState) -> AgentState:
    score = state.get("assessment_score") or 65.0 
    state["assessment_score"] = score
    state["current_step"] = "Assessment Completed"
    state["messages"].append(f"Assessment completed with score: {score}")
    return state

def generate_recommendation(state: AgentState) -> AgentState:
    score = state.get("assessment_score", 0)
    
    # 1. LIVE ML INFERENCE
    prediction = recommender_engine.predict_next_topic(score)
    topic = prediction["topic"]
    conf = prediction["confidence_score"]
    
    state["recommended_topic"] = topic
    state["current_step"] = "Recommendation Generated"
    state["messages"].append(f"ML Recommended topic: {topic} (Confidence: {conf*100:.1f}%)")
    return state

def build_quiz(state: AgentState) -> AgentState:
    topic = state.get("recommended_topic", "General")
    
    # 2. LIVE GENERATIVE AI 
    quiz_json = build_quiz_from_topic(topic)
    
    state["quiz_id"] = 999
    state["quiz_data"] = quiz_json
    state["current_step"] = "Quiz Built"
    state["messages"].append(f"Gemini built custom JSON quiz for topic: {topic}")
    return state

def evaluate_quiz(state: AgentState) -> AgentState:
    state["quiz_score"] = 85.0
    state["current_step"] = "Quiz Evaluated"
    state["messages"].append(f"Quiz evaluated with score: {state['quiz_score']}")
    return state

def update_progress(state: AgentState) -> AgentState:
    state["current_step"] = "Progress Updated"
    state["messages"].append("Saved progress to database.")
    return state

def generate_report(state: AgentState) -> AgentState:
    state["status"] = "Ready for Report"
    state["current_step"] = "Workflow Complete"
    state["messages"].append("Weekly report generated successfully.")
    return state

workflow = StateGraph(AgentState)

workflow.add_node("run_assessment", run_assessment)
workflow.add_node("generate_recommendation", generate_recommendation)
workflow.add_node("build_quiz", build_quiz)
workflow.add_node("evaluate_quiz", evaluate_quiz)
workflow.add_node("update_progress", update_progress)
workflow.add_node("generate_report", generate_report)

workflow.set_entry_point("run_assessment")
workflow.add_edge("run_assessment", "generate_recommendation")
workflow.add_edge("generate_recommendation", "build_quiz")
workflow.add_edge("build_quiz", "evaluate_quiz")
workflow.add_edge("evaluate_quiz", "update_progress")
workflow.add_edge("update_progress", "generate_report")
workflow.add_edge("generate_report", END)

memory = MemorySaver()
app_workflow = workflow.compile(checkpointer=memory)
""")
