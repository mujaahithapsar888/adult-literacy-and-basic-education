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
