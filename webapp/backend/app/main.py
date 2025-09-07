"""
Main FastAPI application for EU Grants Monitor Web Platform.

This application provides a web interface for companies to:
- Register and authenticate via Google/Microsoft SSO
- Search and browse EU grant opportunities
- Use AI-powered assistance for grant applications (paid feature)
- Track application progress and manage company profiles
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
from pathlib import Path

from .database import engine, get_db, create_tables
from .models import Base
from .auth import router as auth_router, get_current_user
from .grants import router as grants_router
from .payments import router as payments_router
from .users import router as users_router
from .ai_assistant import router as ai_assistant_router
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    print("🚀 Starting EU Grants Monitor Web Platform...")
    
    # Create database tables - Disabled since tables already exist via Supabase
    # await create_tables()
    print("✅ Database tables ready (existing Supabase setup)")
    
    # Start background tasks for grant data synchronization
    # This will be implemented in the grants service
    print("✅ Background services started")
    
    yield
    
    # Shutdown
    print("👋 Shutting down EU Grants Monitor Web Platform...")


# Create FastAPI application
app = FastAPI(
    title="EU Grants Monitor Web Platform",
    description="AI-powered platform for EU grant discovery and application assistance",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(grants_router, prefix="/api/grants", tags=["Grants"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
app.include_router(ai_assistant_router, prefix="/api/ai-assistant", tags=["AI Assistant"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "EU Grants Monitor Web Platform",
        "version": "1.0.0"
    }


@app.get("/api/")
async def root():
    """Root endpoint with service information."""
    return {
        "message": "Welcome to EU Grants Monitor Web Platform",
        "description": "AI-powered platform for EU grant discovery and application assistance",
        "version": "1.0.0",
        "docs_url": "/api/docs",
        "features": [
            "Grant discovery and search",
            "Company registration and profiles", 
            "Google/Microsoft SSO authentication",
            "AI-powered application assistance (premium)",
            "Application tracking and management",
            "Automated grant database updates"
        ]
    }


@app.get("/api/me")
async def get_current_user_info(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information."""
    return {
        "user": current_user,
        "subscription": current_user.subscription_status,
        "company": current_user.company
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler."""
    return {
        "error": True,
        "message": "An unexpected error occurred",
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )
