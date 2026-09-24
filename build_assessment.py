import os

def rewrite(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Schemas
rewrite("backend/app/schemas/assessment.py", """
from pydantic import BaseModel
from typing import List, Dict, Any

class AssessmentSubmission(BaseModel):
    assessment_id: int
    answers: Dict[str, str] # e.g. {"q1": "Option A"}

class AssessmentResult(BaseModel):
    assessment_id: int
    score: float
    passed: bool
    feedback: str
""")

# 2. Repository
rewrite("backend/app/repositories/assessment_repo.py", """
from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.models.progress import StudentProgress
from app.models.course import Course
import random # For mocking

def get_assessment(db: Session, assessment_id: int):
    # In a real app, query by ID. For now we will return a mock or create one if it doesn't exist
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        course = db.query(Course).first()
        if not course:
            course = Course(title="Mock Course", description="Mock")
            db.add(course)
            db.commit()
        assessment = Assessment(id=assessment_id, course_id=course.id, title="Mock Assessment", max_score=100)
        db.add(assessment)
        db.commit()
    return assessment

def save_progress(db: Session, user_id: int, course_id: int, score: float, passed: bool):
    status = "Completed" if passed else "In Progress"
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == user_id, 
        StudentProgress.course_id == course_id
    ).first()
    
    if progress:
        progress.score = score
        progress.status = status
    else:
        progress = StudentProgress(
            user_id=user_id,
            course_id=course_id,
            status=status,
            score=score
        )
        db.add(progress)
    db.commit()
    return progress
""")

# 3. Service
rewrite("backend/app/services/assessment_service.py", """
from sqlalchemy.orm import Session
from app.repositories import assessment_repo
from app.schemas.assessment import AssessmentSubmission, AssessmentResult

def grade_assessment(db: Session, user_id: int, submission: AssessmentSubmission):
    assessment = assessment_repo.get_assessment(db, submission.assessment_id)
    
    # Mock grading logic: every answer is worth 10 points for simplicity
    score = len(submission.answers) * 10.0
    if score > assessment.max_score:
        score = float(assessment.max_score)
        
    passed = score >= (assessment.max_score * 0.7) # 70% to pass
    
    # Save progress
    assessment_repo.save_progress(db, user_id, assessment.course_id, score, passed)
    
    feedback = "Excellent work!" if passed else "Keep practicing, you'll get it next time!"
    
    return AssessmentResult(
        assessment_id=assessment.id,
        score=score,
        passed=passed,
        feedback=feedback
    )
""")

# 4. Routes
rewrite("backend/app/routes/assessment.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.assessment import AssessmentSubmission, AssessmentResult
from app.services import assessment_service
from app.authentication.security import get_current_user

router = APIRouter(prefix="/assessment", tags=["Assessment"])

@router.post("/start")
def start_assessment(category: str, difficulty: str, current_user = Depends(get_current_user)):
    # This would generate or fetch an assessment based on criteria
    return {"status": "started", "assessment_id": 101, "message": f"Started {difficulty} {category} assessment."}

@router.post("/submit", response_model=AssessmentResult)
def submit_assessment(submission: AssessmentSubmission, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return assessment_service.grade_assessment(db, current_user.id, submission)

@router.get("/result/{assessment_id}", response_model=AssessmentResult)
def get_result(assessment_id: int, current_user = Depends(get_current_user)):
    # Mock return, normally query from progress or a results table
    return AssessmentResult(assessment_id=assessment_id, score=85.0, passed=True, feedback="Good job")
""")

# 5. Frontend API
rewrite("frontend/services/api.py", """
import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def get_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
        if response.status_code == 200:
            return response.json()
        return {"error": response.json().get("detail", "Login failed")}
    except Exception as e:
        return {"error": str(e)}

def register(email, password, role="Student"):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "role": role})
        if response.status_code == 200:
            return response.json()
        return {"error": response.json().get("detail", "Registration failed")}
    except Exception as e:
        return {"error": str(e)}

def forgot_password(email):
    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json={"email": email})
        if response.status_code == 200:
            return response.json()
        return {"error": response.json().get("detail", "Failed")}
    except Exception as e:
        return {"error": str(e)}

def start_assessment(category, difficulty):
    try:
        res = requests.post(f"{BASE_URL}/assessment/start", params={"category": category, "difficulty": difficulty}, headers=get_headers())
        if res.status_code == 200:
            return res.json()
        return {"error": res.text}
    except Exception as e:
        return {"error": str(e)}

def submit_assessment(assessment_id, answers):
    try:
        res = requests.post(
            f"{BASE_URL}/assessment/submit", 
            json={"assessment_id": assessment_id, "answers": answers}, 
            headers=get_headers()
        )
        if res.status_code == 200:
            return res.json()
        return {"error": res.text}
    except Exception as e:
        return {"error": str(e)}
""")

# 6. Update frontend/pages/learning.py 
# We'll use file reading and replacing to keep the layout but hook up the new API endpoints
with open("frontend/pages/learning.py", "r", encoding="utf-8") as f:
    learning_code = f.read()

# Let's completely replace `render_skill_assessment`
old_render = """def render_skill_assessment():
    st.title("📝 Skill Assessment")"""

# We'll inject the new function
import_statement = "from services.api import start_assessment, submit_assessment\n"
if "start_assessment" not in learning_code:
    learning_code = import_statement + learning_code

# We need to find the definition of render_skill_assessment and replace it.
# It ends right before `def render_personalized_learning_path():`
start_idx = learning_code.find("def render_skill_assessment():")
end_idx = learning_code.find("def render_personalized_learning_path():")

new_render = """def render_skill_assessment():
    st.title("📝 Skill Assessment")
    
    if 'assessment_state' not in st.session_state:
        st.session_state['assessment_state'] = 'selection'
    if 'assessment_id' not in st.session_state:
        st.session_state['assessment_id'] = None
    if 'assessment_result' not in st.session_state:
        st.session_state['assessment_result'] = None
    
    if st.session_state['assessment_state'] == 'selection':
        st.subheader("Select Assessment Category")
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Reading", "Writing", "Mathematics", "English", "Digital Literacy", "Life Skills"])
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Start Assessment", type="primary"):
            with st.spinner("Starting assessment..."):
                res = start_assessment(category, difficulty)
                if "error" in res:
                    st.error("Error connecting to backend: " + res["error"])
                else:
                    st.session_state['assessment_id'] = res.get("assessment_id", 101)
                    st.session_state['assessment_state'] = 'taking'
                    st.rerun()
            
    elif st.session_state['assessment_state'] == 'taking':
        c1, c2 = st.columns([3, 1])
        c1.subheader("Question 1 of 10")
        c2.info("⏱ Time Remaining: 14:23")
        
        st.progress(10, text="Progress: 10%")
        st.markdown("---")
        st.markdown("### Which of the following is the correct answer?")
        
        ans = st.radio("Select your answer:", [
            "Option A: Correct answer here.",
            "Option B: Incorrect answer.",
            "Option C: Another incorrect answer.",
            "Option D: None of the above."
        ], index=None)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 6, 3])
        nav1.button("⬅ Previous")
        if nav3.button("Submit Assessment ✅", type="primary"):
            if not ans:
                st.warning("Please select an answer.")
            else:
                with st.spinner("Grading..."):
                    # Send submission to backend
                    answers = {"q1": ans}
                    res = submit_assessment(st.session_state['assessment_id'], answers)
                    if "error" in res:
                        st.error("Error: " + res["error"])
                    else:
                        st.session_state['assessment_result'] = res
                        st.session_state['assessment_state'] = 'results'
                        st.rerun()
            
    elif st.session_state['assessment_state'] == 'results':
        st.subheader("📊 Assessment Results")
        result = st.session_state['assessment_result']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{result['score']}%")
        c2.metric("Status", "Passed" if result['passed'] else "Needs Practice")
        c3.metric("Feedback", result['feedback'])
        
        st.markdown("---")
        
        # Radar Chart
        categories = ['Reading', 'Writing', 'Mathematics', 'English', 'Digital Literacy', 'Life Skills']
        # Mock varied scores for visualization
        scores = [result['score'], 82, 65, 80, 90, 85]
        
        df_radar = pd.DataFrame(dict(Score=scores, Skill=categories))
        fig = px.line_polar(df_radar, r='Score', theta='Skill', line_close=True, markers=True, color_discrete_sequence=['#4361ee'])
        fig.update_traces(fill='toself', fillcolor='rgba(67, 97, 238, 0.3)')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), margin=dict(l=20, r=20, t=20, b=20), height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("🔄 Retake Assessment"):
            st.session_state['assessment_state'] = 'selection'
            st.rerun()

"""

learning_code = learning_code[:start_idx] + new_render + learning_code[end_idx:]

with open("frontend/pages/learning.py", "w", encoding="utf-8") as f:
    f.write(learning_code)

print("Assessment module updated successfully.")
