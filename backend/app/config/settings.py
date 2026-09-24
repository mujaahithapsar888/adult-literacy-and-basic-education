from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduDash API"
    DATABASE_URL: str = "sqlite:///./test.db"  # Using SQLite for easy local dev, replace with Postgres for production
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
