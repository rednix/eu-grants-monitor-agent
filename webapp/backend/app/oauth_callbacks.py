"""
OAuth callback endpoints for Google and Microsoft authentication.
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Dict, Any
import httpx
from urllib.parse import urlencode

from .database import get_db
from .auth import create_or_update_user, create_access_token
from .config import settings

router = APIRouter()


@router.get("/google")
async def google_oauth_login():
    """Initiate Google OAuth login."""
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url=google_auth_url)


@router.get("/google/callback")
async def google_oauth_callback(
    request: Request, 
    code: str = None, 
    error: str = None,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback."""
    if error:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error={error}")
    
    if not code:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=no_code")
    
    try:
        # Exchange code for token
        async with httpx.AsyncClient() as client:
            token_data = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            }
            
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data=token_data
            )
            
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get access token")
            
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            
            # Get user info
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            user_info = user_response.json()
            
            # Create or update user
            user = create_or_update_user(user_info, "google", db)
            
            # Create JWT token
            token_data = {"sub": user.id}
            jwt_token = create_access_token(token_data)
            
            # Redirect to frontend with token
            redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={jwt_token}"
            return RedirectResponse(url=redirect_url)
            
    except Exception as e:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=auth_failed")


@router.get("/microsoft")
async def microsoft_oauth_login():
    """Initiate Microsoft OAuth login."""
    if not settings.MICROSOFT_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Microsoft OAuth not configured")
    
    params = {
        "client_id": settings.MICROSOFT_CLIENT_ID,
        "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile User.Read",
        "response_mode": "query"
    }
    
    microsoft_auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urlencode(params)}"
    return RedirectResponse(url=microsoft_auth_url)


@router.get("/microsoft/callback")
async def microsoft_oauth_callback(
    request: Request,
    code: str = None,
    error: str = None,
    db: Session = Depends(get_db)
):
    """Handle Microsoft OAuth callback."""
    if error:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error={error}")
    
    if not code:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=no_code")
    
    try:
        # Exchange code for token
        async with httpx.AsyncClient() as client:
            token_data = {
                "client_id": settings.MICROSOFT_CLIENT_ID,
                "client_secret": settings.MICROSOFT_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            }
            
            token_response = await client.post(
                "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                data=token_data
            )
            
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get access token")
            
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            
            # Get user info
            user_response = await client.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            user_info = user_response.json()
            
            # Create or update user
            user = create_or_update_user(user_info, "microsoft", db)
            
            # Create JWT token
            token_data = {"sub": user.id}
            jwt_token = create_access_token(token_data)
            
            # Redirect to frontend with token
            redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={jwt_token}"
            return RedirectResponse(url=redirect_url)
            
    except Exception as e:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=auth_failed")
