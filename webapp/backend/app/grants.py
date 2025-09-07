"""
Grants API endpoints for search, filtering, and management.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from pydantic import BaseModel
from datetime import datetime, date

from .database import get_db
from .models import Grant, User, GrantStatus
from .auth import get_current_user, get_optional_current_user

router = APIRouter()


class GrantSearchRequest(BaseModel):
    """Grant search request model."""
    query: Optional[str] = None
    keywords: Optional[List[str]] = None
    programs: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    min_funding: Optional[int] = None
    max_funding: Optional[int] = None
    max_complexity: Optional[int] = None
    deadline_days_min: Optional[int] = None
    deadline_days_max: Optional[int] = None
    technology_areas: Optional[List[str]] = None
    industry_sectors: Optional[List[str]] = None
    target_organizations: Optional[List[str]] = None
    page: int = 1
    limit: int = 20
    sort_by: str = "deadline"  # deadline, funding_amount, complexity_score, relevance


class GrantResponse(BaseModel):
    """Grant response model."""
    id: int
    grant_id: str
    title: str
    program: str
    synopsis: Optional[str]
    description: str
    total_budget: int
    min_funding_amount: Optional[int]
    max_funding_amount: Optional[int]
    deadline: datetime
    days_until_deadline: int
    eligible_countries: List[str]
    target_organizations: List[str]
    keywords: List[str]
    technology_areas: List[str]
    industry_sectors: List[str]
    url: Optional[str]
    documents_url: Optional[str]
    status: GrantStatus
    complexity_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class GrantListResponse(BaseModel):
    """Grant list response model."""
    grants: List[GrantResponse]
    total_count: int
    page: int
    limit: int
    total_pages: int


@router.get("/", response_model=GrantListResponse)
async def list_grants(
    query: Optional[str] = Query(None, description="Search query"),
    program: Optional[str] = Query(None, description="Filter by program"),
    country: Optional[str] = Query(None, description="Filter by eligible country"),
    min_funding: Optional[int] = Query(None, description="Minimum funding amount"),
    max_funding: Optional[int] = Query(None, description="Maximum funding amount"),
    max_complexity: Optional[int] = Query(None, description="Maximum complexity score"),
    technology_area: Optional[str] = Query(None, description="Filter by technology area"),
    industry_sector: Optional[str] = Query(None, description="Filter by industry sector"),
    status: Optional[GrantStatus] = Query(GrantStatus.OPEN, description="Grant status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("deadline", description="Sort by field"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """List grants with optional filtering and search."""
    
    # Base query
    query_builder = db.query(Grant).filter(Grant.status == status)
    
    # Apply filters
    if query:
        # Simple text search in title, description, and keywords
        search_filter = or_(
            Grant.title.ilike(f"%{query}%"),
            Grant.description.ilike(f"%{query}%"),
            Grant.synopsis.ilike(f"%{query}%")
        )
        query_builder = query_builder.filter(search_filter)
    
    if program:
        query_builder = query_builder.filter(Grant.program.ilike(f"%{program}%"))
    
    if country:
        query_builder = query_builder.filter(Grant.eligible_countries.contains([country]))
    
    if min_funding:
        query_builder = query_builder.filter(
            or_(Grant.min_funding_amount >= min_funding, Grant.min_funding_amount.is_(None))
        )
    
    if max_funding:
        query_builder = query_builder.filter(
            or_(Grant.max_funding_amount <= max_funding, Grant.max_funding_amount.is_(None))
        )
    
    if max_complexity:
        query_builder = query_builder.filter(
            or_(Grant.complexity_score <= max_complexity, Grant.complexity_score.is_(None))
        )
    
    if technology_area:
        query_builder = query_builder.filter(Grant.technology_areas.contains([technology_area]))
    
    if industry_sector:
        query_builder = query_builder.filter(Grant.industry_sectors.contains([industry_sector]))
    
    # Get total count before pagination
    total_count = query_builder.count()
    
    # Apply sorting
    if sort_by == "deadline":
        query_builder = query_builder.order_by(Grant.deadline)
    elif sort_by == "funding_amount":
        query_builder = query_builder.order_by(desc(Grant.total_budget))
    elif sort_by == "complexity_score":
        query_builder = query_builder.order_by(Grant.complexity_score.nulls_last())
    elif sort_by == "created_at":
        query_builder = query_builder.order_by(desc(Grant.created_at))
    else:
        query_builder = query_builder.order_by(Grant.deadline)
    
    # Apply pagination
    offset = (page - 1) * limit
    grants = query_builder.offset(offset).limit(limit).all()
    
    # Calculate days until deadline for each grant
    grant_responses = []
    for grant in grants:
        grant_dict = {
            "id": grant.id,
            "grant_id": grant.grant_id,
            "title": grant.title,
            "program": grant.program,
            "synopsis": grant.synopsis,
            "description": grant.description,
            "total_budget": grant.total_budget,
            "min_funding_amount": grant.min_funding_amount,
            "max_funding_amount": grant.max_funding_amount,
            "deadline": grant.deadline,
            "days_until_deadline": grant.days_until_deadline,
            "eligible_countries": grant.eligible_countries or [],
            "target_organizations": grant.target_organizations or [],
            "keywords": grant.keywords or [],
            "technology_areas": grant.technology_areas or [],
            "industry_sectors": grant.industry_sectors or [],
            "url": grant.url,
            "documents_url": grant.documents_url,
            "status": grant.status,
            "complexity_score": grant.complexity_score,
            "created_at": grant.created_at
        }
        grant_responses.append(GrantResponse(**grant_dict))
    
    total_pages = (total_count + limit - 1) // limit
    
    return GrantListResponse(
        grants=grant_responses,
        total_count=total_count,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


@router.post("/search", response_model=GrantListResponse)
async def search_grants(
    search_request: GrantSearchRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Advanced grant search with multiple filters."""
    
    # Base query
    query_builder = db.query(Grant).filter(Grant.status == GrantStatus.OPEN)
    
    # Apply search query
    if search_request.query:
        search_filter = or_(
            Grant.title.ilike(f"%{search_request.query}%"),
            Grant.description.ilike(f"%{search_request.query}%"),
            Grant.synopsis.ilike(f"%{search_request.query}%")
        )
        query_builder = query_builder.filter(search_filter)
    
    # Apply keyword filters
    if search_request.keywords:
        for keyword in search_request.keywords:
            keyword_filter = or_(
                Grant.keywords.contains([keyword]),
                Grant.title.ilike(f"%{keyword}%"),
                Grant.description.ilike(f"%{keyword}%")
            )
            query_builder = query_builder.filter(keyword_filter)
    
    # Apply program filters
    if search_request.programs:
        query_builder = query_builder.filter(Grant.program.in_(search_request.programs))
    
    # Apply country filters
    if search_request.countries:
        country_filters = []
        for country in search_request.countries:
            country_filters.append(Grant.eligible_countries.contains([country]))
        query_builder = query_builder.filter(or_(*country_filters))
    
    # Apply funding amount filters
    if search_request.min_funding:
        query_builder = query_builder.filter(
            or_(Grant.max_funding_amount >= search_request.min_funding, Grant.max_funding_amount.is_(None))
        )
    
    if search_request.max_funding:
        query_builder = query_builder.filter(
            or_(Grant.min_funding_amount <= search_request.max_funding, Grant.min_funding_amount.is_(None))
        )
    
    # Apply complexity filter
    if search_request.max_complexity:
        query_builder = query_builder.filter(
            or_(Grant.complexity_score <= search_request.max_complexity, Grant.complexity_score.is_(None))
        )
    
    # Apply deadline filters
    if search_request.deadline_days_min or search_request.deadline_days_max:
        today = datetime.now().date()
        
        if search_request.deadline_days_min:
            min_deadline = today + timedelta(days=search_request.deadline_days_min)
            query_builder = query_builder.filter(Grant.deadline >= min_deadline)
        
        if search_request.deadline_days_max:
            max_deadline = today + timedelta(days=search_request.deadline_days_max)
            query_builder = query_builder.filter(Grant.deadline <= max_deadline)
    
    # Apply technology area filters
    if search_request.technology_areas:
        tech_filters = []
        for tech_area in search_request.technology_areas:
            tech_filters.append(Grant.technology_areas.contains([tech_area]))
        query_builder = query_builder.filter(or_(*tech_filters))
    
    # Apply industry sector filters
    if search_request.industry_sectors:
        industry_filters = []
        for industry in search_request.industry_sectors:
            industry_filters.append(Grant.industry_sectors.contains([industry]))
        query_builder = query_builder.filter(or_(*industry_filters))
    
    # Apply target organization filters
    if search_request.target_organizations:
        org_filters = []
        for org_type in search_request.target_organizations:
            org_filters.append(Grant.target_organizations.contains([org_type]))
        query_builder = query_builder.filter(or_(*org_filters))
    
    # Get total count
    total_count = query_builder.count()
    
    # Apply sorting
    if search_request.sort_by == "deadline":
        query_builder = query_builder.order_by(Grant.deadline)
    elif search_request.sort_by == "funding_amount":
        query_builder = query_builder.order_by(desc(Grant.total_budget))
    elif search_request.sort_by == "complexity_score":
        query_builder = query_builder.order_by(Grant.complexity_score.nulls_last())
    else:
        query_builder = query_builder.order_by(Grant.deadline)
    
    # Apply pagination
    offset = (search_request.page - 1) * search_request.limit
    grants = query_builder.offset(offset).limit(search_request.limit).all()
    
    # Convert to response format
    grant_responses = []
    for grant in grants:
        grant_dict = {
            "id": grant.id,
            "grant_id": grant.grant_id,
            "title": grant.title,
            "program": grant.program,
            "synopsis": grant.synopsis,
            "description": grant.description,
            "total_budget": grant.total_budget,
            "min_funding_amount": grant.min_funding_amount,
            "max_funding_amount": grant.max_funding_amount,
            "deadline": grant.deadline,
            "days_until_deadline": grant.days_until_deadline,
            "eligible_countries": grant.eligible_countries or [],
            "target_organizations": grant.target_organizations or [],
            "keywords": grant.keywords or [],
            "technology_areas": grant.technology_areas or [],
            "industry_sectors": grant.industry_sectors or [],
            "url": grant.url,
            "documents_url": grant.documents_url,
            "status": grant.status,
            "complexity_score": grant.complexity_score,
            "created_at": grant.created_at
        }
        grant_responses.append(GrantResponse(**grant_dict))
    
    total_pages = (total_count + search_request.limit - 1) // search_request.limit
    
    return GrantListResponse(
        grants=grant_responses,
        total_count=total_count,
        page=search_request.page,
        limit=search_request.limit,
        total_pages=total_pages
    )


@router.get("/{grant_id}", response_model=GrantResponse)
async def get_grant(
    grant_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Get detailed information about a specific grant."""
    
    grant = db.query(Grant).filter(Grant.grant_id == grant_id).first()
    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")
    
    grant_dict = {
        "id": grant.id,
        "grant_id": grant.grant_id,
        "title": grant.title,
        "program": grant.program,
        "synopsis": grant.synopsis,
        "description": grant.description,
        "total_budget": grant.total_budget,
        "min_funding_amount": grant.min_funding_amount,
        "max_funding_amount": grant.max_funding_amount,
        "deadline": grant.deadline,
        "days_until_deadline": grant.days_until_deadline,
        "eligible_countries": grant.eligible_countries or [],
        "target_organizations": grant.target_organizations or [],
        "keywords": grant.keywords or [],
        "technology_areas": grant.technology_areas or [],
        "industry_sectors": grant.industry_sectors or [],
        "url": grant.url,
        "documents_url": grant.documents_url,
        "status": grant.status,
        "complexity_score": grant.complexity_score,
        "created_at": grant.created_at
    }
    
    return GrantResponse(**grant_dict)


@router.get("/filters/options")
async def get_filter_options(db: Session = Depends(get_db)):
    """Get available filter options for grant search."""
    
    # Get unique values for various filter fields
    programs = db.query(Grant.program).distinct().all()
    countries = db.query(Grant.eligible_countries).filter(Grant.eligible_countries.is_not(None)).all()
    technology_areas = db.query(Grant.technology_areas).filter(Grant.technology_areas.is_not(None)).all()
    industry_sectors = db.query(Grant.industry_sectors).filter(Grant.industry_sectors.is_not(None)).all()
    target_organizations = db.query(Grant.target_organizations).filter(Grant.target_organizations.is_not(None)).all()
    
    # Flatten and deduplicate arrays
    all_countries = set()
    for row in countries:
        if row[0]:
            all_countries.update(row[0])
    
    all_tech_areas = set()
    for row in technology_areas:
        if row[0]:
            all_tech_areas.update(row[0])
    
    all_industries = set()
    for row in industry_sectors:
        if row[0]:
            all_industries.update(row[0])
    
    all_target_orgs = set()
    for row in target_organizations:
        if row[0]:
            all_target_orgs.update(row[0])
    
    return {
        "programs": sorted([p[0] for p in programs if p[0]]),
        "countries": sorted(list(all_countries)),
        "technology_areas": sorted(list(all_tech_areas)),
        "industry_sectors": sorted(list(all_industries)),
        "target_organizations": sorted(list(all_target_orgs)),
        "complexity_ranges": [
            {"label": "Low (0-40)", "min": 0, "max": 40},
            {"label": "Medium (41-70)", "min": 41, "max": 70},
            {"label": "High (71-100)", "min": 71, "max": 100}
        ],
        "funding_ranges": [
            {"label": "€0 - €100k", "min": 0, "max": 100000},
            {"label": "€100k - €500k", "min": 100000, "max": 500000},
            {"label": "€500k - €1M", "min": 500000, "max": 1000000},
            {"label": "€1M+", "min": 1000000, "max": None}
        ]
    }
