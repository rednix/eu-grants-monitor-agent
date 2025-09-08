"""
Authentication system with Google and Microsoft OAuth support.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import httpx
import uuid
from passlib.context import CryptContext

from .database import get_db
from .models import User, Company, UserRole, SubscriptionStatus, CompanySize
from .config import settings

router = APIRouter()
security = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


class UserCreate(BaseModel):
    """User creation model."""
    email: EmailStr
    full_name: str
    password: Optional[str] = None  # For email/password signup
    google_id: Optional[str] = None
    microsoft_id: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str


class CompanyCreate(BaseModel):
    """Company creation model."""
    name: str
    size: CompanySize
    country: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not user.hashed_password:
        return None  # OAuth-only user
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise None."""
    if not credentials:
        return None
    
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        return None


async def get_google_user_info(access_token: str) -> Dict[str, Any]:
    """Get user info from Google OAuth."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Google token")
        return response.json()


async def get_microsoft_user_info(access_token: str) -> Dict[str, Any]:
    """Get user info from Microsoft OAuth."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Microsoft token")
        return response.json()


def create_or_update_user(user_info: Dict[str, Any], provider: str, db: Session) -> User:
    """Create or update user from OAuth provider."""
    email = user_info.get("email") or user_info.get("mail")
    if not email:
        raise HTTPException(status_code=400, detail="Email not provided by OAuth provider")
    
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Update existing user
        if provider == "google" and not user.google_id:
            user.google_id = user_info.get("id")
        elif provider == "microsoft" and not user.microsoft_id:
            user.microsoft_id = user_info.get("id")
        
        # Update profile info if not set
        if not user.profile_picture_url:
            if provider == "google":
                user.profile_picture_url = user_info.get("picture")
            elif provider == "microsoft":
                # Microsoft Graph API photo endpoint would need separate call
                pass
        
        user.email_verified = True
        user.last_login = datetime.utcnow()
        
    else:
        # Create new user
        full_name = user_info.get("name") or f"{user_info.get('given_name', '')} {user_info.get('family_name', '')}".strip()
        if not full_name and provider == "microsoft":
            full_name = user_info.get("displayName", email.split("@")[0])
        
        user = User(
            email=email,
            full_name=full_name,
            google_id=user_info.get("id") if provider == "google" else None,
            microsoft_id=user_info.get("id") if provider == "microsoft" else None,
            profile_picture_url=user_info.get("picture") if provider == "google" else None,
            email_verified=True,
            role=UserRole.USER,
            subscription_status=SubscriptionStatus.FREE,
            last_login=datetime.utcnow()
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user


@router.post("/google", response_model=TokenResponse)
async def login_google(request: Request, db: Session = Depends(get_db)):
    """Login with Google OAuth."""
    body = await request.json()
    access_token = body.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token required")
    
    # Get user info from Google
    user_info = await get_google_user_info(access_token)
    
    # Create or update user
    user = create_or_update_user(user_info, "google", db)
    
    # Create JWT token
    token_data = {"sub": user.id}
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "role": user.role,
            "subscription_status": user.subscription_status,
            "has_company": user.company_id is not None
        }
    )


@router.post("/microsoft", response_model=TokenResponse)
async def login_microsoft(request: Request, db: Session = Depends(get_db)):
    """Login with Microsoft OAuth."""
    body = await request.json()
    access_token = body.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token required")
    
    # Get user info from Microsoft
    user_info = await get_microsoft_user_info(access_token)
    
    # Create or update user
    user = create_or_update_user(user_info, "microsoft", db)
    
    # Create JWT token
    token_data = {"sub": user.id}
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "role": user.role,
            "subscription_status": user.subscription_status,
            "has_company": user.company_id is not None
        }
    )


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    if not user_data.password:
        raise HTTPException(
            status_code=400,
            detail="Password is required for signup"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=UserRole.USER,
        subscription_status=SubscriptionStatus.FREE,
        email_verified=False,  # Can be verified via email later
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create JWT token
    token_data = {"sub": user.id}
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "role": user.role,
            "subscription_status": user.subscription_status,
            "has_company": user.company_id is not None
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user with email and password."""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create JWT token
    token_data = {"sub": user.id}
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "role": user.role,
            "subscription_status": user.subscription_status,
            "has_company": user.company_id is not None
        }
    )


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token."""
    token_data = {"sub": current_user.id}
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "profile_picture_url": current_user.profile_picture_url,
            "role": current_user.role,
            "subscription_status": current_user.subscription_status,
            "has_company": current_user.company_id is not None
        }
    )


@router.post("/logout")
async def logout():
    """Logout user (client should discard token)."""
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "profile_picture_url": current_user.profile_picture_url,
        "role": current_user.role,
        "subscription_status": current_user.subscription_status,
        "ai_assistant_credits": current_user.ai_assistant_credits,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at,
        "company": {
            "id": current_user.company.id,
            "name": current_user.company.name,
            "size": current_user.company.size,
            "country": current_user.company.country,
            "profile_completed": current_user.company.profile_completed,
            "profile_completion_percentage": current_user.company.profile_completion_percentage
        } if current_user.company else None
    }
