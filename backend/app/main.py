from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import (
    agent, auth, students, assessment, recommendations,
    prediction, quiz, chat, analytics, reports
)
from app.database.connection import Base, engine

# Import models so they are registered with Base.metadata before create_all
import app.models.user
import app.models.course
import app.models.assessment
import app.models.progress
import app.models.ai_tutor

from app.middleware.exceptions import custom_exception_handler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created.")
    yield
    logger.info("Application shutdown: Cleaning up resources...")

app = FastAPI(
    title="EduDash API",
    description="Production-ready FastAPI backend for EduDash",
    version="1.0.0",
    lifespan=lifespan
)

# Exception Handler
app.add_exception_handler(Exception, custom_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "EduDash API is running in production mode!"}

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(assessment.router)
app.include_router(recommendations.router)
app.include_router(prediction.router)
app.include_router(quiz.router)
app.include_router(chat.router)
app.include_router(analytics.router)
app.include_router(reports.router)
app.include_router(agent.router)
