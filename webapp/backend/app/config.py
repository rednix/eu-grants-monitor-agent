"""
Configuration settings for EU Grants Monitor Web Platform.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "EU Grants Monitor Web Platform"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/eu_grants_monitor"
    )
    
    # Supabase Configuration (overrides DATABASE_URL if set)
    SUPABASE_DATABASE_URL: Optional[str] = os.getenv("SUPABASE_DATABASE_URL")
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    PROJECT_REF: Optional[str] = os.getenv("PROJECT_REF")
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "your-super-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",
        "https://frontend-3yx2epjnp-nicos-projects-bbdc04b5.vercel.app",  # Vercel frontend
        "https://grants.yourdomain.com",
        "https://yourdomain.com"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # OAuth Settings
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv(
        "GOOGLE_REDIRECT_URI", 
        "https://grant-monitor-production.up.railway.app/api/auth/google/callback"
    )
    
    MICROSOFT_CLIENT_ID: str = os.getenv("MICROSOFT_CLIENT_ID", "")
    MICROSOFT_CLIENT_SECRET: str = os.getenv("MICROSOFT_CLIENT_SECRET", "")
    MICROSOFT_REDIRECT_URI: str = os.getenv(
        "MICROSOFT_REDIRECT_URI",
        "https://grant-monitor-production.up.railway.app/api/auth/microsoft/callback"
    )
    
    # Stripe Payment Settings
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Pricing (in cents)
    AI_ASSISTANT_PRICE_MONTHLY: int = 4900  # $49.00/month
    AI_ASSISTANT_PRICE_YEARLY: int = 49900  # $499.00/year
    AI_ASSISTANT_PRICE_PER_APPLICATION: int = 1900  # $19.00 per application
    
    # Email Settings (for notifications)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@yourdomain.com")
    
    # Redis (for caching and sessions)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI Assistant Settings (integration with existing agent)
    AI_ASSISTANT_ENDPOINT: str = os.getenv(
        "AI_ASSISTANT_ENDPOINT", 
        "http://localhost:8001"
    )
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Grant Data Sources
    HORIZON_EUROPE_API_URL: str = "https://ec.europa.eu/info/funding-tenders/opportunities/rest-services"
    DIGITAL_EUROPE_API_URL: str = "https://digital-strategy.ec.europa.eu/en/activities/digital-programme"
    
    # Background Tasks
    GRANT_SYNC_INTERVAL_HOURS: int = 6
    GRANT_SYNC_ENABLED: bool = True
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".doc", ".docx", ".txt"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour
    
    # Application URLs
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()


# Global settings instance
settings = get_settings()
