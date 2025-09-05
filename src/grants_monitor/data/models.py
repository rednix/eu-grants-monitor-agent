"""
Data models for the EU Grants Monitor Agent.

This module defines the core data structures used throughout the application.
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, validator


class ComplexityLevel(str, Enum):
    """Grant application complexity levels."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class FundingProgram(str, Enum):
    """EU funding programs."""
    HORIZON_EUROPE = "horizon_europe"
    DIGITAL_EUROPE = "digital_europe"
    ERDF = "erdf"
    ERASMUS_PLUS = "erasmus_plus"
    COSME = "cosme"
    INNOVATION_FUND = "innovation_fund"
    ESF_PLUS = "esf_plus"
    LIFE = "life"
    CEF = "cef"
    OTHER = "other"


class Grant(BaseModel):
    """A grant opportunity model."""
    
    id: str = Field(..., description="Unique grant identifier")
    title: str = Field(..., description="Grant title")
    description: str = Field(..., description="Grant description")
    program: FundingProgram = Field(..., description="Funding program")
    
    # Financial details
    funding_amount: float = Field(..., description="Available funding amount in EUR")
    min_funding: Optional[float] = Field(None, description="Minimum funding amount")
    max_funding: Optional[float] = Field(None, description="Maximum funding amount")
    
    # Timing
    deadline: date = Field(..., description="Application deadline")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    
    # Eligibility and requirements
    eligible_countries: List[str] = Field(default_factory=list, description="Eligible countries")
    target_organizations: List[str] = Field(default_factory=list, description="Target organization types")
    keywords: List[str] = Field(default_factory=list, description="Keywords and topics")
    
    # URLs and references
    url: str = Field(..., description="Official grant URL")
    documents_url: Optional[str] = Field(None, description="Application documents URL")
    
    # Analysis scores (populated by agent)
    relevance_score: float = Field(0.0, description="Relevance score (0-100)")
    complexity_score: float = Field(0.0, description="Complexity score (0-100)")
    priority_score: float = Field(0.0, description="Overall priority score (0-100)")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def days_until_deadline(self) -> int:
        """Calculate days until deadline."""
        return (self.deadline - date.today()).days
    
    @property
    def complexity_level(self) -> ComplexityLevel:
        """Get complexity level based on score."""
        if self.complexity_score < 30:
            return ComplexityLevel.SIMPLE
        elif self.complexity_score < 70:
            return ComplexityLevel.MEDIUM
        else:
            return ComplexityLevel.COMPLEX


class BusinessProfile(BaseModel):
    """Business profile for matching grants."""
    
    # Company details
    company_name: str = Field(..., description="Company name")
    company_size: str = Field(..., description="Company size (micro, small, medium)")
    country: str = Field(..., description="Company country")
    
    # AI expertise
    ai_expertise: List[str] = Field(default_factory=list, description="AI expertise areas")
    technology_focus: List[str] = Field(default_factory=list, description="Technology focus areas")
    
    # Industry and sectors
    target_industries: List[str] = Field(default_factory=list, description="Target industries")
    business_sectors: List[str] = Field(default_factory=list, description="Business sectors")
    
    # Funding preferences
    preferred_funding_range: Dict[str, float] = Field(
        default_factory=lambda: {"min": 10000, "max": 500000},
        description="Preferred funding range"
    )
    max_project_duration_months: int = Field(24, description="Maximum project duration in months")
    
    # Application preferences
    complexity_preference: ComplexityLevel = Field(
        ComplexityLevel.SIMPLE, 
        description="Preferred application complexity"
    )
    team_size: int = Field(1, description="Available team size for projects")
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "BusinessProfile":
        """Create business profile from configuration."""
        return cls(**config)


class Alert(BaseModel):
    """Alert notification model."""
    
    id: str = Field(..., description="Alert identifier")
    grant_id: str = Field(..., description="Related grant ID")
    alert_type: str = Field(..., description="Type of alert")
    message: str = Field(..., description="Alert message")
    priority: str = Field(..., description="Alert priority")
    sent_at: datetime = Field(default_factory=datetime.now)


class ApplicationStatus(str, Enum):
    """Application status tracking."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(BaseModel):
    """Grant application tracking model."""
    
    id: str = Field(..., description="Application identifier")
    grant_id: str = Field(..., description="Related grant ID")
    status: ApplicationStatus = Field(ApplicationStatus.DRAFT, description="Application status")
    
    # Application details
    submitted_at: Optional[datetime] = Field(None, description="Submission timestamp")
    deadline_reminder_sent: bool = Field(False, description="Whether deadline reminder was sent")
    
    # Outcome
    decision_date: Optional[date] = Field(None, description="Decision date")
    awarded_amount: Optional[float] = Field(None, description="Awarded amount if successful")
    feedback: Optional[str] = Field(None, description="Application feedback")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ScrapingSession(BaseModel):
    """Scraping session tracking."""
    
    id: str = Field(..., description="Session identifier")
    source: str = Field(..., description="Data source")
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    # Results
    grants_found: int = Field(0, description="Number of grants found")
    grants_new: int = Field(0, description="Number of new grants")
    grants_updated: int = Field(0, description="Number of updated grants")
    
    # Status
    status: str = Field("running", description="Session status")
    error_message: Optional[str] = Field(None, description="Error message if failed")
