# Comprehensive System Architecture & Low-Level Design (LLD)
**Project:** AI-Powered Personalized Learning Platform (Adult Literacy and Basic Education)

---

## 1. Requirement Analysis

### 1.1 Core Objectives
*   **Adaptive Learning:** Dynamically recommend topics based on student performance using Machine Learning (Scikit-Learn).
*   **Dynamic Content Generation:** Create contextual, tailored multiple-choice quizzes on the fly using Generative AI (Google Gemini).
*   **NLP Evaluation:** Evaluate student responses for sentiment, reading level, and misconceptions (Hugging Face Transformers/spaCy).
*   **Autonomous Orchestration:** Seamlessly string together ML, GenAI, and Database states without human intervention (LangGraph).

### 1.2 Functional Requirements
*   **Authentication:** Secure registration, login, and Role-Based Access Control (Student, Teacher, Admin).
*   **Assessment System:** Initial baseline testing and continuous progress tracking.
*   **Dashboard:** Intuitive user interface for students to view metrics, take quizzes, and see recommendations.

### 1.3 Non-Functional Requirements
*   **Scalability:** Microservice-ready backend via FastAPI and Docker.
*   **Security:** JWT-based stateless authentication, bcrypt password hashing, and secure API boundaries.
*   **Performance:** Fast API response times and asynchronous model inference.

---

## 2. System Architecture

The platform utilizes a multi-tier, client-server architecture with an integrated AI orchestrator. 
*   **Presentation Tier:** Streamlit (Python)
*   **Application Tier:** FastAPI (RESTful API, Auth, Business Logic)
*   **Data Tier:** PostgreSQL / SQLite
*   **AI Engine Tier:** LangGraph (State Machine), Gemini (GenAI), Scikit-Learn (ML), Transformers (NLP)

---

## 3. C4 Model

### 3.1 System Context Diagram (Level 1)
```mermaid
C4Context
    title System Context Diagram
    Person(student, "Student", "Adult learner taking courses.")
    Person(teacher, "Teacher", "Monitors student progress.")
    System(platform, "AI Learning Platform", "Provides adaptive quizzes and recommendations.")
    System_Ext(gemini, "Google Gemini API", "Generates custom quiz content.")
    
    Rel(student, platform, "Takes quizzes, views progress")
    Rel(teacher, platform, "Reviews student metrics")
    Rel(platform, gemini, "Requests JSON quizzes based on ML topics")
```

### 3.2 Container Diagram (Level 2)
```mermaid
C4Container
    title Container Diagram
    Person(user, "User", "Student or Teacher")
    
    Container(frontend, "Streamlit Dashboard", "Python", "Provides the UI.")
    Container(backend, "FastAPI Application", "Python", "Handles business logic, auth, and AI orchestration.")
    ContainerDb(database, "PostgreSQL Database", "Relational DB", "Stores users, courses, and progress metrics.")
    Container(ml_models, "Scikit-Learn Models", "Pickle/PKL", "Predicts optimal learning paths.")
    Container(nlp_pipeline, "Hugging Face Transformers", "Python", "Analyzes sentiment and reading levels.")
    
    Rel(user, frontend, "Interacts via HTTPS")
    Rel(frontend, backend, "REST API Calls (JSON)")
    Rel(backend, database, "Reads/Writes (SQLAlchemy ORM)")
    Rel(backend, ml_models, "Loads for inference")
    Rel(backend, nlp_pipeline, "Processes text inputs")
    Rel(backend, "Google Gemini", "API request (gRPC/REST)")
```

---

## 4. UML Diagrams

### 4.1 Use Case Diagram
```mermaid
usecaseDiagram
    actor Student
    actor Teacher
    
    Student --> (Register/Login)
    Student --> (Take Baseline Assessment)
    Student --> (View Recommended Topic)
    Student --> (Take AI-Generated Quiz)
    
    Teacher --> (Register/Login)
    Teacher --> (View Student Analytics)
    Teacher --> (Manage Course Content)
```

---

## 5. ER Diagram & Database Schema

### 5.1 Entity-Relationship (ER) Diagram
```mermaid
erDiagram
    USER ||--o{ STUDENT_PROGRESS : "tracks"
    USER ||--o{ ASSESSMENT : "takes"
    COURSE ||--o{ LESSON : "contains"
    COURSE ||--o{ STUDENT_PROGRESS : "associated with"
    LESSON ||--o{ QUIZ : "has"
    
    USER {
        int id PK
        string email
        string hashed_password
        string role
        datetime created_at
    }
    COURSE {
        int id PK
        string title
        string difficulty_level
    }
    LESSON {
        int id PK
        int course_id FK
        string title
        text content_body
    }
    ASSESSMENT {
        int id PK
        int user_id FK
        float score
        datetime timestamp
    }
    QUIZ {
        int id PK
        int lesson_id FK
        json generated_content
    }
    STUDENT_PROGRESS {
        int id PK
        int user_id FK
        int course_id FK
        float proficiency_score
    }
```

### 5.2 Database Design Details
*   **ORM:** SQLAlchemy
*   **Migrations:** Alembic
*   **Keys:** Strict foreign-key constraints linking Users to their Progress and Assessments to ensure data integrity.

---

## 6. Component Diagram

Illustrates the internal structure of the FastAPI backend.

```mermaid
graph TD
    subgraph FastAPI Backend
        Router[API Routers]
        Auth[Authentication Middleware]
        Services[Business Logic Services]
        Repo[Database Repositories]
        Agent[LangGraph Orchestrator]
        ML[ML Recommender]
        GenAI[Gemini Quiz Builder]
    end
    
    Router --> Auth
    Router --> Services
    Router --> Agent
    Services --> Repo
    Agent --> ML
    Agent --> GenAI
    Agent --> Repo
    Repo --> DB[(SQL Database)]
```

---

## 7. Sequence Diagram

This outlines the core autonomous AI loop when a student requests the next lesson.

```mermaid
sequenceDiagram
    participant UI as Streamlit Frontend
    participant API as FastAPI (Router)
    participant Agent as LangGraph Orchestrator
    participant ML as Scikit-Learn Recommender
    participant GenAI as Google Gemini API
    participant DB as Database
    
    UI->>API: POST /agent/orchestrate {user_id}
    API->>Agent: Trigger State Machine
    Agent->>DB: Fetch user progress & metrics
    DB-->>Agent: Return metrics data
    Agent->>ML: Predict next optimal topic
    ML-->>Agent: Return "Phonics" (85% confidence)
    Agent->>GenAI: Request 5-question quiz for "Phonics"
    GenAI-->>Agent: Return JSON quiz payload
    Agent->>DB: Save generated quiz
    DB-->>Agent: Confirm save
    Agent-->>API: Return final graph state
    API-->>UI: Display Quiz to Student
```

---

## 8. API Design & Documentation

The API follows strict RESTful conventions using FastAPI. OpenAPI/Swagger documentation is auto-generated at `/docs`.

### 8.1 Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Creates a new User. | No |
| `POST` | `/auth/login` | Returns JWT Access Token. | No |
| `GET`  | `/users/me` | Returns current user profile. | Yes |
| `POST` | `/assessment/submit` | Grades and stores an assessment. | Yes |
| `POST` | `/agent/orchestrate` | Kicks off the LangGraph AI pipeline. | Yes |

### 8.2 Standard Response Model (JSON)
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully."
}
```

---

## 9. Security Design

### 9.1 Authentication & Authorization
*   **Stateless Sessions:** JWT (JSON Web Tokens) with a 30-minute expiration.
*   **Password Security:** Passwords are never stored in plaintext. Hashed via `bcrypt`.
*   **Dependency Injection:** FastAPI `Depends()` enforces that routes requiring authentication automatically validate the JWT in the `Authorization: Bearer <token>` header.

### 9.2 API Security
*   **CORS Configuration:** Strictly defined origins allowed.
*   **Environment Variables:** Secrets (`SECRET_KEY`, `GEMINI_API_KEY`, `DATABASE_URL`) are isolated in a `.env` file and never committed to version control.

---

## 10. Deployment Architecture & Plan

### 10.1 Deployment Architecture Diagram
```mermaid
graph LR
    User((User/Browser))
    subgraph Docker Host
        Streamlit[Streamlit Container :8501]
        FastAPI[FastAPI Container :8000]
        Postgres[(PostgreSQL Container :5432)]
    end
    
    User -- HTTP --> Streamlit
    Streamlit -- Internal Network --> FastAPI
    FastAPI -- Internal Network --> Postgres
```

### 10.2 Deployment Plan
1.  **Containerization:** `Dockerfile` is provided for both backend and frontend.
2.  **Orchestration:** `docker-compose.yml` links the web layer, API layer, and database layer into an isolated virtual network.
3.  **Environment Setup:** Provision a `.env` file on the production server.
4.  **Execution:** Run `docker-compose up -d --build` to pull images, build the containers, run Alembic migrations, and start the application in detached mode.
5.  **Reverse Proxy:** In a true production environment, an NGINX reverse proxy would sit in front of the Docker Host to handle SSL/TLS termination and route traffic to ports 8000/8501.
