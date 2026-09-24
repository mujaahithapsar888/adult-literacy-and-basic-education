import os

def rewrite(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Create the LangGraph Workflow
rewrite("backend/app/agent/workflow.py", """
from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Define the State Schema
class AgentState(TypedDict):
    student_id: int
    current_step: str
    assessment_score: Optional[float]
    recommended_topic: Optional[str]
    quiz_id: Optional[int]
    quiz_score: Optional[float]
    status: str
    messages: List[str]

# Define Node Functions

def run_assessment(state: AgentState) -> AgentState:
    # In a real app, query database to find recent assessment scores
    score = 75.5 # Mock score
    state["assessment_score"] = score
    state["current_step"] = "Assessment Completed"
    state["messages"].append(f"Assessment completed with score: {score}")
    return state

def generate_recommendation(state: AgentState) -> AgentState:
    score = state.get("assessment_score", 0)
    topic = "Advanced Reading" if score > 70 else "Basic Reading"
    state["recommended_topic"] = topic
    state["current_step"] = "Recommendation Generated"
    state["messages"].append(f"Recommended topic: {topic}")
    return state

def build_quiz(state: AgentState) -> AgentState:
    topic = state.get("recommended_topic", "General")
    # Mocking Gemini API call
    state["quiz_id"] = 101
    state["current_step"] = "Quiz Built"
    state["messages"].append(f"Built quiz {state['quiz_id']} for topic: {topic}")
    return state

def evaluate_quiz(state: AgentState) -> AgentState:
    # Mock grading the quiz
    state["quiz_score"] = 85.0
    state["current_step"] = "Quiz Evaluated"
    state["messages"].append(f"Quiz evaluated with score: {state['quiz_score']}")
    return state

def update_progress(state: AgentState) -> AgentState:
    # Update StudentProgress table
    state["current_step"] = "Progress Updated"
    state["messages"].append("Saved progress to database.")
    return state

def generate_report(state: AgentState) -> AgentState:
    # Compile a final report
    state["status"] = "Ready for Report"
    state["current_step"] = "Workflow Complete"
    state["messages"].append("Weekly report generated successfully.")
    return state

# Compile the Graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("run_assessment", run_assessment)
workflow.add_node("generate_recommendation", generate_recommendation)
workflow.add_node("build_quiz", build_quiz)
workflow.add_node("evaluate_quiz", evaluate_quiz)
workflow.add_node("update_progress", update_progress)
workflow.add_node("generate_report", generate_report)

# Add linear edges
workflow.set_entry_point("run_assessment")
workflow.add_edge("run_assessment", "generate_recommendation")
workflow.add_edge("generate_recommendation", "build_quiz")
workflow.add_edge("build_quiz", "evaluate_quiz")
workflow.add_edge("evaluate_quiz", "update_progress")
workflow.add_edge("update_progress", "generate_report")
workflow.add_edge("generate_report", END)

# Initialize persistent memory saver
memory = MemorySaver()

# Compile
app_workflow = workflow.compile(checkpointer=memory)
""")

# 2. Create the API Router for Orchestration
rewrite("backend/app/routes/agent.py", """
from fastapi import APIRouter, Depends, HTTPException
from app.authentication.security import get_current_user
from app.agent.workflow import app_workflow
from pydantic import BaseModel

router = APIRouter(prefix="/agent", tags=["Agent Orchestration"])

class OrchestrationResponse(BaseModel):
    student_id: int
    status: str
    final_step: str
    history: list

@router.post("/orchestrate", response_model=OrchestrationResponse)
def run_orchestration(current_user = Depends(get_current_user)):
    thread_id = f"student_{current_user.id}"
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "student_id": current_user.id,
        "current_step": "Initialized",
        "assessment_score": None,
        "recommended_topic": None,
        "quiz_id": None,
        "quiz_score": None,
        "status": "In Progress",
        "messages": []
    }
    
    # Execute the LangGraph workflow
    result = app_workflow.invoke(initial_state, config=config)
    
    return OrchestrationResponse(
        student_id=result["student_id"],
        status=result["status"],
        final_step=result["current_step"],
        history=result["messages"]
    )
""")

# 3. Update main.py to include the new router
with open("backend/app/main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

if "import agent" not in main_code and "app.include_router(agent.router)" not in main_code:
    main_code = main_code.replace("from app.routes import ", "from app.routes import agent, ")
    main_code = main_code.replace("app.include_router(reports.router)", "app.include_router(reports.router)\napp.include_router(agent.router)")
    
    with open("backend/app/main.py", "w", encoding="utf-8") as f:
        f.write(main_code)
