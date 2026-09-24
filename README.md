# AI-Powered Personalized Learning Platform
## For Adult Literacy and Basic Education

This project is a complete, production-ready enterprise application designed to provide an intelligent, personalized learning experience. The platform combines a modern Streamlit frontend with a robust FastAPI backend, utilizing Machine Learning and Generative AI orchestrated through LangGraph.

---

## 🚀 Features

### **1. Agentic AI Orchestration (LangGraph)**
At the heart of the platform is an autonomous state machine that routes students through their learning lifecycle:
- **Assessment**: Evaluates student performance.
- **Recommendation**: Uses Scikit-Learn to predict the optimal next topic with a confidence score.
- **Dynamic Quizzes**: Leverages Google Gemini to generate custom JSON-structured quizzes based on the recommendation.
- **Progress Tracking**: Evaluates quizzes and dynamically updates student metrics in the database.

### **2. Machine Learning & Generative AI**
- **Scikit-Learn**: A Random Forest Classifier analyzes student assessment scores and historical performance to dynamically prescribe learning paths.
- **Google Gemini API**: Instantly generates rigorous, multi-choice educational content tailored to the exact topic recommended by the ML model.

### **3. Robust Backend (FastAPI)**
- **Authentication**: JWT-based auth with bcrypt password hashing, role-based access control (Student, Teacher, Admin), and secure endpoints.
- **Database**: Fully normalized relational schema using SQLAlchemy (User, Course, Lesson, Assessment, Quiz, StudentProgress, Recommendation). 
- **Production-Ready**: Features centralized exception handling middleware, async server lifespan, Alembic migrations, and comprehensive automated testing.

### **4. Modern Frontend (Streamlit)**
- **Educational Dashboard**: A sleek, responsive user interface inspired by modern platforms like Duolingo and Coursera.
- **Interactive UI**: Features dynamic metric cards, sidebars, interactive charts (Plotly), and integrated assessment views.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit, Plotly, Pandas, Requests, Custom CSS
- **Backend**: FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn, JWT, bcrypt
- **AI & Orchestration**: LangGraph, Google Gemini SDK (`google-generativeai`), Scikit-Learn, NumPy
- **Database**: PostgreSQL (Production via Docker) / SQLite (Local Development)
- **Deployment**: Docker, Docker Compose

---

## 🔄 Project Workflow & AI Pipeline Architecture

The platform operates on a continuous, data-driven cycle designed to automatically adapt to a student's learning progress. Below is the detailed breakdown of the data pipeline and workflow.

### 1. User Onboarding and Authentication
- **Action**: A user registers or logs in via the Streamlit frontend.
- **Pipeline**: The frontend sends an API request to `POST /auth/register` or `POST /auth/login`.
- **Backend Logic**: The FastAPI router hashes the password using `bcrypt` and stores the user in the PostgreSQL database. Upon login, a secure JWT (JSON Web Token) is generated and returned to the client for stateful session management.

### 2. Initial Assessment
- **Action**: The student takes a baseline assessment to gauge their current proficiency.
- **Pipeline**: The frontend submits the answers to `POST /assessment/submit`.
- **Backend Logic**: The backend grades the assessment in real-time and writes the raw score to the `StudentProgress` database table. This score becomes the foundational metric for all future AI recommendations.

### 3. Agentic AI Orchestration (The LangGraph Pipeline)
When a student completes a module or assessment, the frontend triggers the orchestration layer via `POST /agent/orchestrate`. This kicks off a fully autonomous LangGraph state machine with the following node progression:

*   **Node A (`run_assessment`)**: Fetches the student's most recent assessment scores and historical data from the database.
*   **Node B (`generate_recommendation`)**: 
    *   **Data Flow**: Passes the raw assessment metrics into the `LearningRecommender` (Scikit-Learn).
    *   **Processing**: The Random Forest Classifier evaluates the features and predicts the mathematically optimal next learning topic (e.g., "Advanced Reading").
    *   **State Update**: Appends the `recommended_topic` and a `confidence_score` to the graph's memory state.
*   **Node C (`build_quiz`)**:
    *   **Data Flow**: Extracts the `recommended_topic` from the graph state and passes it to the `quiz_builder` (Google Gemini SDK).
    *   **Processing**: Gemini processes a strict system prompt to dynamically generate a 5-question multiple-choice quiz about that exact topic.
    *   **State Update**: Validates the JSON response and stores it in the graph state as `quiz_data`.
*   **Node D (`evaluate_quiz`)**: Evaluates the student's eventual performance on this newly generated content.
*   **Node E (`update_progress`)**: Updates the relational database with the new metrics.
*   **Node F (`generate_report`)**: Compiles the cycle into a weekly performance report for teacher review.

### 4. Continuous Feedback Loop
Because LangGraph utilizes a `MemorySaver` checkpointer tied to the user's `thread_id`, the system retains a persistent memory of the student's journey. Each time the cycle repeats, the Scikit-Learn model receives *updated* historical data, making its future recommendations increasingly accurate over time.

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional for production)

### 1. Environment Setup
Create a `.env` file in the root directory and add the following variables:
```env
# Authentication
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./edudash.db  # Use PostgreSQL URL for production

# AI APIs
GEMINI_API_KEY=your_gemini_api_key_here  # Leave empty or set to "mock" for offline fallback mode
```

### 2. Running Locally (Development)
**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Note: The FastAPI Swagger documentation will be available at `http://localhost:8000/docs`*

**Frontend:**
Open a new terminal window:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
*Note: The frontend will be available at `http://localhost:8501`*

### 3. Running via Docker (Production)
The project includes a `docker-compose.yml` for easy deployment, firing up a PostgreSQL database and the FastAPI server:
```bash
docker-compose up -d --build
```

---

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agent/            # LangGraph State Machine (workflow.py)
│   │   ├── authentication/   # JWT and Security logic
│   │   ├── database/         # SQLAlchemy connection & config
│   │   ├── genai/            # Google Gemini Quiz Builder
│   │   ├── ml/               # Scikit-Learn Recommender
│   │   ├── models/           # SQLAlchemy Database Models
│   │   ├── routes/           # FastAPI API Endpoints
│   │   ├── schemas/          # Pydantic validation models
│   │   └── main.py           # Application Factory
│   └── tests/                # Pytest automated testing suite
├── frontend/
│   ├── app.py                # Main Streamlit Dashboard
│   └── services/             # API request hooks
├── docker-compose.yml
└── README.md
```

---

## 🧪 Testing

To run the automated backend test suite:
```bash
cd backend
pytest tests/
```
