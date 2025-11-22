"""
Configuration settings loaded from environment variables
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App settings
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/lunaverse"
    
    # Vector DB
    VECTOR_DB_URL: str = "http://vector-db:8000"
    VECTOR_DB_API_KEY: str = ""
    VECTOR_DB_TYPE: str = "chroma"  # or "qdrant"
    
    # Hugging Face
    HF_API_URL: str = ""
    HF_API_KEY: str = ""
    HF_MODEL_NAME: str = "meta-llama/Llama-3-8b-instruct"
    HF_TEMPERATURE: float = 0.3
    HF_MAX_NEW_TOKENS: int = 2000
    
    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:4173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # RAG Settings
    INVENTORY_TOP_K: int = 40
    HISTORIC_TOP_K: int = 10
    TEMPLATES_TOP_K: int = 10
    
    # Current RMS (v2+)
    CURRENT_RMS_SUBDOMAIN: str = ""
    CURRENT_RMS_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

