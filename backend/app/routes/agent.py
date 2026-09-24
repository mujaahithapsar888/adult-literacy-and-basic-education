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
