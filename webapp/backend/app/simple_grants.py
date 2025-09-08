"""
Simple grants API that reads from Supabase database.
This provides fast access to grants data from the PostgreSQL database.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

router = APIRouter()


class SimpleGrant(BaseModel):
    """Simplified grant model."""
    id: int
    grant_id: str
    title: str
    program: str
    description: str
    synopsis: Optional[str]
    total_budget: int
    min_funding_amount: Optional[int]
    max_funding_amount: Optional[int]
    deadline: str
    days_until_deadline: int
    eligible_countries: List[str]
    target_organizations: List[str]
    keywords: List[str]
    technology_areas: List[str]
    industry_sectors: List[str]
    url: Optional[str]
    documents_url: Optional[str]
    status: str
    complexity_score: Optional[float]
    created_at: str


class SimpleGrantListResponse(BaseModel):
    """Simple grant list response."""
    grants: List[SimpleGrant]
    total_count: int
    page: int
    limit: int
    total_pages: int


# Database configuration - initialize only when needed
engine = None
SessionLocal = None

def get_database_url():
    """Get database URL from environment variables."""
    # First check environment variables for Supabase
    database_url = os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL")
    
    # If no environment variable, try to import from main config
    if not database_url:
        try:
            from .config import settings
            database_url = settings.DATABASE_URL
        except ImportError:
            pass
    
    # If still no database URL, provide a helpful error
    if not database_url:
        raise ValueError(
            "No database URL found in environment variables. "
            "Please set SUPABASE_DATABASE_URL or DATABASE_URL environment variable."
        )
    
    # Make sure we're not defaulting to localhost
    if "localhost" in database_url or "127.0.0.1" in database_url:
        raise ValueError(
            f"Invalid database URL pointing to localhost: {database_url}. "
            "This should point to your Supabase database."
        )
    
    return database_url

def initialize_database():
    """Initialize database connection."""
    global engine, SessionLocal
    if engine is None:
        database_url = get_database_url()
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, let the dependency handle it

def get_db_session():
    """Dependency for getting database session."""
    initialize_database()  # Ensure database is initialized
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_json_field(value: Any) -> List[str]:
    """Parse JSON field from database."""
    try:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return json.loads(value) if value else []
        return []
    except (json.JSONDecodeError, TypeError):
        return []


@router.get("/simple", response_model=SimpleGrantListResponse)
async def list_grants_simple(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    query: Optional[str] = Query(None, description="Search query"),
    program: Optional[str] = Query(None, description="Filter by program"),
    min_amount: Optional[int] = Query(None, description="Minimum funding amount"),
    max_amount: Optional[int] = Query(None, description="Maximum funding amount"),
    technology_areas: Optional[str] = Query(None, description="Technology areas (comma-separated)"),
    db: Session = Depends(get_db_session)
):
    """List grants from Supabase database."""
    
    try:
        # Build query
        where_clauses = []
        params = {}
        
        if query:
            where_clauses.append("(title ILIKE :query OR description ILIKE :query OR synopsis ILIKE :query)")
            params["query"] = f"%{query}%"
        
        if program:
            where_clauses.append("program ILIKE :program")
            params["program"] = f"%{program}%"
        
        if min_amount:
            where_clauses.append("(min_funding_amount >= :min_amount OR min_funding_amount IS NULL)")
            params["min_amount"] = min_amount
        
        if max_amount:
            where_clauses.append("(max_funding_amount <= :max_amount OR max_funding_amount IS NULL)")
            params["max_amount"] = max_amount
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Get total count
        count_sql = f"SELECT COUNT(*) FROM grants {where_clause}"
        result = db.execute(text(count_sql), params)
        total_count = result.scalar()
        
        # Get grants with pagination
        offset = (page - 1) * limit
        grants_sql = f"""
            SELECT * FROM grants 
            {where_clause}
            ORDER BY deadline ASC
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        result = db.execute(text(grants_sql), params)
        grant_rows = result.mappings().all()
        grants = []
        
        for row in grant_rows:
            # Calculate days until deadline
            try:
                if isinstance(row['deadline'], str):
                    deadline_dt = datetime.fromisoformat(row['deadline'].replace('Z', '+00:00'))
                else:
                    deadline_dt = row['deadline']
                days_until = (deadline_dt.date() - datetime.now().date()).days
            except:
                days_until = 0
            
            grant = SimpleGrant(
                id=row['id'],
                grant_id=row['grant_id'],
                title=row['title'],
                program=row['program'],
                description=row['description'],
                synopsis=row['synopsis'],
                total_budget=row['total_budget'],
                min_funding_amount=row['min_funding_amount'],
                max_funding_amount=row['max_funding_amount'],
                deadline=row['deadline'] if isinstance(row['deadline'], str) else row['deadline'].isoformat(),
                days_until_deadline=days_until,
                eligible_countries=parse_json_field(row['eligible_countries']),
                target_organizations=parse_json_field(row['target_organizations']),
                keywords=parse_json_field(row['keywords']),
                technology_areas=parse_json_field(row['technology_areas']),
                industry_sectors=parse_json_field(row['industry_sectors']),
                url=row['url'],
                documents_url=row['documents_url'],
                status=row['status'],
                complexity_score=row['complexity_score'],
                created_at=row['created_at'] if isinstance(row['created_at'], str) else row['created_at'].isoformat()
            )
            grants.append(grant)
        
        total_pages = (total_count + limit - 1) // limit
        
        return SimpleGrantListResponse(
            grants=grants,
            total_count=total_count,
            page=page,
            limit=limit,
            total_pages=total_pages
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/simple/{grant_id}", response_model=SimpleGrant)
async def get_grant_simple(grant_id: str, db: Session = Depends(get_db_session)):
    """Get a specific grant by ID."""
    
    try:
        result = db.execute(text("SELECT * FROM grants WHERE grant_id = :grant_id"), {"grant_id": grant_id})
        row = result.mappings().first()
        
        if not row:
            raise HTTPException(status_code=404, detail="Grant not found")
        
        # Calculate days until deadline
        try:
            if isinstance(row['deadline'], str):
                deadline_dt = datetime.fromisoformat(row['deadline'].replace('Z', '+00:00'))
            else:
                deadline_dt = row['deadline']
            days_until = (deadline_dt.date() - datetime.now().date()).days
        except:
            days_until = 0
        
        return SimpleGrant(
            id=row['id'],
            grant_id=row['grant_id'],
            title=row['title'],
            program=row['program'],
            description=row['description'],
            synopsis=row['synopsis'],
            total_budget=row['total_budget'],
            min_funding_amount=row['min_funding_amount'],
            max_funding_amount=row['max_funding_amount'],
            deadline=row['deadline'] if isinstance(row['deadline'], str) else row['deadline'].isoformat(),
            days_until_deadline=days_until,
            eligible_countries=parse_json_field(row['eligible_countries']),
            target_organizations=parse_json_field(row['target_organizations']),
            keywords=parse_json_field(row['keywords']),
            technology_areas=parse_json_field(row['technology_areas']),
            industry_sectors=parse_json_field(row['industry_sectors']),
            url=row['url'],
            documents_url=row['documents_url'],
            status=row['status'],
            complexity_score=row['complexity_score'],
            created_at=row['created_at'] if isinstance(row['created_at'], str) else row['created_at'].isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/simple/stats")
async def get_grants_stats(db: Session = Depends(get_db_session)):
    """Get grants statistics."""
    
    try:
        # Total grants
        result = db.execute(text("SELECT COUNT(*) FROM grants"))
        total_grants = result.scalar()
        
        # Grants by program
        result = db.execute(text("SELECT program, COUNT(*) FROM grants GROUP BY program"))
        by_program = dict(result.fetchall())
        
        # Grants by status
        result = db.execute(text("SELECT status, COUNT(*) FROM grants GROUP BY status"))
        by_status = dict(result.fetchall())
        
        # Average complexity score
        result = db.execute(text("SELECT AVG(complexity_score) FROM grants WHERE complexity_score IS NOT NULL"))
        avg_complexity = result.scalar() or 0
        
        return {
            "total_grants": total_grants,
            "by_program": by_program,
            "by_status": by_status,
            "average_complexity_score": round(avg_complexity, 1)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
