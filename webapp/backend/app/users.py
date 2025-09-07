"""Users API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .auth import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get user profile."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "subscription_status": current_user.subscription_status
    }
