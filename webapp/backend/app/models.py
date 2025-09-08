"""
Database models for EU Grants Monitor Web Platform.
"""

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, ForeignKey, 
    Integer, JSON, String, Text, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """User roles in the system."""
    USER = "user"
    COMPANY_ADMIN = "company_admin" 
    SYSTEM_ADMIN = "system_admin"


class SubscriptionStatus(str, enum.Enum):
    """Subscription status for AI assistant."""
    FREE = "free"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PAY_PER_USE = "pay_per_use"
    CANCELLED = "cancelled"


class CompanySize(str, enum.Enum):
    """Company size classifications."""
    MICRO = "micro"  # 1-9 employees
    SMALL = "small"  # 10-49 employees  
    MEDIUM = "medium"  # 50-249 employees
    LARGE = "large"  # 250+ employees


class GrantStatus(str, enum.Enum):
    """Grant opportunity status."""
    OPEN = "open"
    CLOSED = "closed"
    UPCOMING = "upcoming"
    CANCELLED = "cancelled"


class ApplicationStatus(str, enum.Enum):
    """Application status tracking."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    profile_picture_url = Column(String(500))
    
    # Authentication
    hashed_password = Column(String(255), nullable=True)  # For email/password auth
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    microsoft_id = Column(String(255), unique=True, nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    
    # User role and permissions
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    # Subscription information
    subscription_status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.FREE)
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    
    # AI Assistant usage tracking
    ai_assistant_credits = Column(Integer, default=0)  # For pay-per-use model
    ai_assistant_usage_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime)
    
    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="users")
    applications = relationship("Application", back_populates="user")
    
    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"


class Company(Base):
    """Company/Organization model."""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    website = Column(String(255))
    
    # Company details
    size = Column(Enum(CompanySize), nullable=False)
    industry = Column(String(100))
    country = Column(String(2), nullable=False)  # ISO country code
    city = Column(String(100))
    address = Column(Text)
    vat_number = Column(String(50))
    registration_number = Column(String(50))
    
    # AI/Technology expertise (JSON array)
    ai_expertise = Column(JSON, default=list)  # e.g., ["machine_learning", "nlp", "computer_vision"]
    technology_focus = Column(JSON, default=list)  # e.g., ["healthcare", "fintech", "manufacturing"]
    
    # Financial information
    annual_revenue = Column(Integer)  # in euros
    funding_history = Column(JSON, default=list)  # Previous funding rounds
    
    # Funding preferences
    preferred_funding_min = Column(Integer, default=50000)
    preferred_funding_max = Column(Integer, default=500000)
    max_project_duration_months = Column(Integer, default=24)
    
    # Company profile completion
    profile_completed = Column(Boolean, default=False)
    profile_completion_percentage = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="company")
    applications = relationship("Application", back_populates="company")
    
    def __repr__(self):
        return f"<Company(name='{self.name}', size='{self.size}')>"


class Grant(Base):
    """EU Grant opportunity model."""
    __tablename__ = "grants"
    
    id = Column(Integer, primary_key=True, index=True)
    grant_id = Column(String(255), unique=True, nullable=False, index=True)  # External ID
    title = Column(String(500), nullable=False, index=True)
    program = Column(String(100), nullable=False, index=True)  # e.g., "Horizon Europe"
    
    # Grant content
    description = Column(Text, nullable=False)
    synopsis = Column(Text)
    objectives = Column(Text)
    
    # Financial information
    total_budget = Column(Integer, nullable=False)  # in euros
    funding_rate = Column(Float, default=70.0)  # percentage
    min_funding_amount = Column(Integer)
    max_funding_amount = Column(Integer)
    
    # Timeline
    publication_date = Column(DateTime)
    deadline = Column(DateTime, nullable=False)
    project_start_date = Column(DateTime)
    project_end_date = Column(DateTime)
    project_duration_months = Column(Integer)
    
    # Eligibility
    eligible_countries = Column(JSON, default=list)  # ISO country codes
    target_organizations = Column(JSON, default=list)  # SME, University, etc.
    eligible_activities = Column(JSON, default=list)
    
    # Categorization
    keywords = Column(JSON, default=list)
    topics = Column(JSON, default=list)
    technology_areas = Column(JSON, default=list)
    industry_sectors = Column(JSON, default=list)
    
    # External links
    url = Column(String(500))
    documents_url = Column(String(500))
    submission_url = Column(String(500))
    
    # Status and metadata
    status = Column(Enum(GrantStatus), default=GrantStatus.OPEN)
    
    # AI analysis results
    complexity_score = Column(Float)  # 0-100, higher = more complex
    ai_relevance_keywords = Column(JSON, default=list)
    estimated_success_rate = Column(Float)
    
    # Data source tracking
    source_system = Column(String(100))  # "horizon_europe", "digital_europe", etc.
    source_url = Column(String(500))
    last_updated = Column(DateTime, default=func.now())
    
    # Search and filtering
    search_vector = Column(Text)  # For full-text search
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    applications = relationship("Application", back_populates="grant")
    
    def __repr__(self):
        return f"<Grant(grant_id='{self.grant_id}', title='{self.title[:50]}')>"
    
    @property
    def days_until_deadline(self) -> int:
        """Calculate days until deadline."""
        if self.deadline:
            delta = self.deadline.date() - date.today()
            return max(0, delta.days)
        return 0


class Application(Base):
    """Grant application model."""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # References
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    grant_id = Column(Integer, ForeignKey("grants.id"), nullable=False)
    
    # Application details
    project_title = Column(String(500))
    project_summary = Column(Text)
    requested_amount = Column(Integer)  # in euros
    project_duration_months = Column(Integer)
    
    # Application status
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    submitted_at = Column(DateTime)
    
    # AI Assistant usage
    ai_assistant_used = Column(Boolean, default=False)
    ai_assistant_session_id = Column(String(255))
    form_completion_percentage = Column(Float, default=0.0)
    
    # Form data (JSON storage for flexibility)
    form_data = Column(JSON, default=dict)
    generated_documents = Column(JSON, default=list)
    
    # External submission tracking
    external_reference = Column(String(255))  # Reference from EU portal
    submission_confirmation = Column(String(255))
    
    # Result tracking
    evaluation_score = Column(Float)
    feedback_received = Column(Text)
    outcome_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="applications")
    company = relationship("Company", back_populates="applications")
    grant = relationship("Grant", back_populates="applications")
    
    # Unique constraint to prevent duplicate applications
    __table_args__ = (
        UniqueConstraint('company_id', 'grant_id', name='unique_company_grant_application'),
    )
    
    def __repr__(self):
        return f"<Application(id={self.id}, status='{self.status}', grant='{self.grant.title[:30] if self.grant else 'N/A'}')>"


class PaymentTransaction(Base):
    """Payment transaction model."""
    __tablename__ = "payment_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User and payment details
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=False)
    stripe_session_id = Column(String(255), unique=True, nullable=True)
    
    # Transaction details
    amount = Column(Integer, nullable=False)  # in cents
    currency = Column(String(3), default="EUR")
    description = Column(String(500))
    
    # Payment status
    status = Column(String(50), default="pending")  # pending, succeeded, failed, cancelled
    
    # Product information
    product_type = Column(String(50))  # monthly, yearly, per_application
    credits_added = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<PaymentTransaction(id={self.id}, amount={self.amount}, status='{self.status}')>"
