"""
Database setup and connection management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import asyncio
from typing import AsyncGenerator

from .config import settings
from .models import Base
import os


# Supabase Configuration
# Priority: SUPABASE_DATABASE_URL > DATABASE_URL
SUPABASE_DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")
DATABASE_URL = SUPABASE_DATABASE_URL or settings.DATABASE_URL

# Display connection info
if SUPABASE_DATABASE_URL:
    db_info = DATABASE_URL.split('@')[1].split(':')[0] if '@' in DATABASE_URL else 'unknown'
    print(f"🟢 Connected to Supabase PostgreSQL: {db_info}")
else:
    print(f"🔵 Using database: {DATABASE_URL.split('://', 1)[0]}")

# Create database engines
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
    async_engine = None  # SQLite doesn't support async in our setup
else:
    # PostgreSQL/Supabase configuration with optimizations
    sync_connect_args = {}
    if "supabase.co" in DATABASE_URL:
        sync_connect_args = {
            "sslmode": "require",
            "application_name": "eu-grants-monitor"
        }
    
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,          # Optimized for Supabase
        max_overflow=20,       # Handle connection spikes  
        pool_recycle=1800,     # Recycle connections every 30 min
        echo=settings.DEBUG,
        connect_args=sync_connect_args
    )
    
    # Async engine for PostgreSQL/Supabase
    async_database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    # Add SSL configuration for Supabase
    connect_args = {}
    if "supabase.co" in DATABASE_URL:
        connect_args = {
            "ssl": "require",
            "server_settings": {
                "application_name": "eu-grants-monitor",
            }
        }
    
    async_engine = create_async_engine(
        async_database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
        echo=settings.DEBUG,
        connect_args=connect_args
    )

# Supabase API configuration (for additional features)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Create session makers
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

if async_engine:
    AsyncSessionLocal = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
else:
    AsyncSessionLocal = None


def get_db() -> Session:
    """
    Get database session for dependency injection.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session for dependency injection.
    
    Yields:
        AsyncSession: SQLAlchemy async database session
    """
    if not AsyncSessionLocal:
        raise RuntimeError("Async database sessions not configured")
    
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    """Create all database tables."""
    if async_engine:
        # Use async engine for PostgreSQL
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    else:
        # Use sync engine for SQLite
        Base.metadata.create_all(bind=engine)


async def drop_tables():
    """Drop all database tables (for testing)."""
    if async_engine:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    else:
        Base.metadata.drop_all(bind=engine)


def init_db():
    """Initialize database with sample data."""
    from .models import User, Company, Grant, CompanySize, GrantStatus
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    try:
        # Check if we already have data
        if db.query(Grant).first():
            print("Database already has data, skipping initialization")
            return
        
        # Create sample grants based on the existing mock data
        sample_grants = [
            Grant(
                grant_id="HE-2024-AI-001",
                title="AI for Healthcare SMEs",
                program="Horizon Europe",
                description="This call supports Small and Medium Enterprises (SMEs) in developing artificial intelligence solutions for healthcare applications. Focus areas include machine learning for medical diagnosis, natural language processing for clinical documentation, and computer vision for medical imaging.",
                synopsis="AI solutions for healthcare: ML diagnosis, NLP clinical docs, CV medical imaging",
                total_budget=10000000,
                min_funding_amount=50000,
                max_funding_amount=500000,
                deadline=datetime.now() + timedelta(days=45),
                project_start_date=datetime.now() + timedelta(days=120),
                project_end_date=datetime.now() + timedelta(days=120 + 730),  # 2 years
                project_duration_months=24,
                eligible_countries=["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI"],
                target_organizations=["SME", "Small Enterprise", "Medium Enterprise"],
                keywords=["artificial intelligence", "healthcare", "machine learning", "medical diagnosis", "clinical validation"],
                technology_areas=["AI", "Healthcare", "Machine Learning"],
                industry_sectors=["Healthcare", "Technology"],
                url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/HORIZON-EIC-2024-PATHFINDEROPEN-01",
                documents_url="https://ec.europa.eu/info/funding-tenders/opportunities/documents",
                status=GrantStatus.OPEN,
                source_system="horizon_europe",
                complexity_score=65.0
            ),
            Grant(
                grant_id="DIGITAL-EU-2024-002",
                title="Digital Innovation for Manufacturing SMEs",
                program="Digital Europe",
                description="Supporting digital transformation in European manufacturing through Industry 4.0 technologies. This call targets SMEs developing solutions in areas such as IoT integration, predictive maintenance using AI, automated quality control, and supply chain optimization.",
                synopsis="Industry 4.0: IoT, AI predictive maintenance, automated quality control",
                total_budget=5000000,
                min_funding_amount=75000,
                max_funding_amount=300000,
                deadline=datetime.now() + timedelta(days=60),
                project_start_date=datetime.now() + timedelta(days=90),
                project_end_date=datetime.now() + timedelta(days=90 + 540),  # 18 months
                project_duration_months=18,
                eligible_countries=["DE", "FR", "IT", "ES", "PL", "CZ", "HU", "SK"],
                target_organizations=["SME", "Manufacturing Company", "Technology Provider"],
                keywords=["digital transformation", "industry 40", "iot", "predictive maintenance", "automation"],
                technology_areas=["IoT", "AI", "Manufacturing"],
                industry_sectors=["Manufacturing", "Technology"],
                url="https://digital-strategy.ec.europa.eu/en/activities/digital-programme",
                status=GrantStatus.OPEN,
                source_system="digital_europe",
                complexity_score=55.0
            ),
            Grant(
                grant_id="LIFE-2024-GREEN-004",
                title="AI-Powered Environmental Monitoring Solutions",
                program="Life",
                description="Developing AI solutions for environmental monitoring and protection. Focus on satellite data analysis, IoT sensor networks, predictive environmental modeling, and automated reporting systems for environmental compliance.",
                synopsis="Green AI: Satellite analysis, IoT sensors, environmental modeling",
                total_budget=3000000,
                min_funding_amount=100000,
                max_funding_amount=400000,
                deadline=datetime.now() + timedelta(days=75),
                project_start_date=datetime.now() + timedelta(days=150),
                project_end_date=datetime.now() + timedelta(days=150 + 720),  # 2 years
                project_duration_months=24,
                eligible_countries=["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI", "PT", "GR"],
                target_organizations=["SME", "Environmental Company", "Technology Provider"],
                keywords=["environmental monitoring", "ai", "satellite data", "iot", "sustainability"],
                technology_areas=["AI", "Environmental", "Satellite"],
                industry_sectors=["Environment", "Technology", "Sustainability"],
                url="https://ec.europa.eu/environment/life/",
                status=GrantStatus.OPEN,
                source_system="life_programme",
                complexity_score=70.0
            )
        ]
        
        for grant in sample_grants:
            db.add(grant)
        
        db.commit()
        print(f"✅ Initialized database with {len(sample_grants)} sample grants")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


def reset_db():
    """Reset database for development/testing."""
    print("🗑️ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️ Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("📊 Initializing sample data...")
    init_db()
    
    print("✅ Database reset complete!")
