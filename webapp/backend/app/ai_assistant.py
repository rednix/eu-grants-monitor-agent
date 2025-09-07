"""AI Assistant API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx

from .database import get_db
from .models import User, Grant, SubscriptionStatus
from .auth import get_current_user
from .config import settings

router = APIRouter()


class AssistanceRequest(BaseModel):
    """AI assistance request."""
    grant_id: str
    assistance_type: str = "analyze"  # analyze, guidance, generate


@router.post("/analyze-grant")
async def analyze_grant(
    request: AssistanceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI analysis of a grant opportunity."""
    
    # Check subscription status
    if current_user.subscription_status == SubscriptionStatus.FREE:
        raise HTTPException(status_code=402, detail="AI Assistant requires subscription")
    
    if (current_user.subscription_status == SubscriptionStatus.PAY_PER_USE and 
        current_user.ai_assistant_credits <= 0):
        raise HTTPException(status_code=402, detail="No AI Assistant credits remaining")
    
    # Get grant
    grant = db.query(Grant).filter(Grant.grant_id == request.grant_id).first()
    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")
    
    # Simulate AI analysis (integrate with existing agent here)
    analysis = {
        "relevance_score": 85.0,
        "complexity_score": grant.complexity_score or 65.0,
        "recommendation": "Highly recommended for your company profile",
        "key_strengths": [
            "Strong alignment with AI expertise",
            "Appropriate funding level for SME",
            "Reasonable application complexity"
        ],
        "considerations": [
            "Ensure compliance with eligibility criteria",
            "Prepare comprehensive technical approach",
            "Plan for required project management"
        ]
    }
    
    # Update usage tracking
    current_user.ai_assistant_usage_count += 1
    if current_user.subscription_status == SubscriptionStatus.PAY_PER_USE:
        current_user.ai_assistant_credits -= 1
    
    db.commit()
    
    return {
        "grant_id": request.grant_id,
        "analysis": analysis,
        "credits_remaining": current_user.ai_assistant_credits
    }
