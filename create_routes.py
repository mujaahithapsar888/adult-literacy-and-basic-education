import os

def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Students
create_file("backend/app/routes/students.py", """
from fastapi import APIRouter

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def get_students():
    return [{"id": 1, "name": "Student A"}]

@router.post("/")
def create_student():
    return {"status": "created"}

@router.put("/{student_id}")
def update_student(student_id: int):
    return {"status": "updated", "id": student_id}

@router.delete("/{student_id}")
def delete_student(student_id: int):
    return {"status": "deleted", "id": student_id}
""")

# Assessment
create_file("backend/app/routes/assessment.py", """
from fastapi import APIRouter

router = APIRouter(prefix="/assessment", tags=["Assessment"])

@router.post("/start")
def start_assessment():
    return {"status": "started", "assessment_id": 101}

@router.post("/submit")
def submit_assessment():
    return {"status": "submitted"}

@router.get("/result")
def get_result():
    return {"score": 85, "details": "Good job"}
""")

# Recommendations
create_file("backend/app/routes/recommendations.py", """
from fastapi import APIRouter
from app.ml.recommender import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/")
def get_recommendations(user_id: int = 1):
    return generate_recommendations(user_id)
""")

# Prediction
create_file("backend/app/routes/prediction.py", """
from fastapi import APIRouter

router = APIRouter(prefix="/prediction", tags=["Prediction"])

@router.post("/")
def make_prediction():
    # Placeholder for DL LSTM prediction
    return {"predicted_score": 92}
""")

# Quiz
create_file("backend/app/routes/quiz.py", """
from fastapi import APIRouter
from app.genai.quiz_generator import generate_quiz

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/generate")
def generate_new_quiz(topic: str = "Math"):
    return generate_quiz(topic)

@router.get("/history")
def quiz_history():
    return [{"quiz_id": 1, "score": 90}]
""")

# Chat
create_file("backend/app/routes/chat.py", """
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["AI Tutor"])

@router.post("/")
def chat_with_tutor(message: str):
    return {"reply": f"AI Tutor says: I can help you with {message}!"}
""")

# Analytics
create_file("backend/app/routes/analytics.py", """
from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def get_analytics():
    return {"learning_hours": 120, "accuracy": 88}
""")

# Reports
create_file("backend/app/routes/reports.py", """
from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/")
def get_reports():
    return {"report_url": "http://localhost/reports/123.pdf"}
""")

# Update main.py to include all routers
with open("backend/app/main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

# Replace the single router include with all routers
import_routes = """from app.routes import auth, students, assessment, recommendations, prediction, quiz, chat, analytics, reports"""

include_routes = """
# Include Routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(assessment.router)
app.include_router(recommendations.router)
app.include_router(prediction.router)
app.include_router(quiz.router)
app.include_router(chat.router)
app.include_router(analytics.router)
app.include_router(reports.router)
"""

main_code = main_code.replace("from app.routes import auth", import_routes)
main_code = main_code.replace("# Include Routers\napp.include_router(auth.router)", include_routes)

with open("backend/app/main.py", "w", encoding="utf-8") as f:
    f.write(main_code)

print("Routes created and hooked up!")
