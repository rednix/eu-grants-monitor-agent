#!/usr/bin/env python3
"""
Database initialization and seeding script for EU Grants Monitor.

This script:
1. Tests the database connection
2. Runs migrations to create tables
3. Seeds the database with sample grant data
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_database_connection():
    """Test if we can connect to the database."""
    try:
        from sqlalchemy import create_engine, text
        from app.config import settings
        
        # Use Supabase URL if available, otherwise fallback to default
        supabase_url = os.getenv("SUPABASE_DATABASE_URL")
        database_url = supabase_url or settings.DATABASE_URL
        
        print(f"🔄 Testing database connection...")
        print(f"   URL: {database_url.split('@')[1] if '@' in database_url else 'local'}")
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version(), current_database();"))
            row = result.fetchone()
            
        print(f"✅ Database connection successful!")
        print(f"   PostgreSQL: {row[0].split(' ')[1]}")
        print(f"   Database: {row[1]}")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure your Supabase project is fully initialized")
        print(f"   2. Check SUPABASE_DATABASE_URL in .env file")
        print(f"   3. Verify database credentials are correct")
        return False


def run_migrations():
    """Run Alembic migrations to create database schema."""
    print(f"\n🏗️  Running database migrations...")
    
    try:
        # Set the Supabase database URL as environment variable for Alembic
        supabase_url = os.getenv("SUPABASE_DATABASE_URL")
        if supabase_url:
            os.environ["DATABASE_URL"] = supabase_url
        
        # Run Alembic upgrade
        exit_code = os.system("alembic upgrade head")
        
        if exit_code == 0:
            print(f"✅ Database schema created successfully!")
            return True
        else:
            print(f"❌ Migration failed with exit code: {exit_code}")
            return False
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False


async def seed_database():
    """Seed the database with sample grant data."""
    print(f"\n🌱 Seeding database with sample data...")
    
    try:
        from app.database import get_async_db
        from app.models import Grant, GrantStatus
        
        # Get database session
        db_gen = get_async_db()
        db = await db_gen.__anext__()
        
        try:
            # Check if we already have grants
            from sqlalchemy import select
            result = await db.execute(select(Grant).limit(1))
            existing_grant = result.scalar_one_or_none()
            
            if existing_grant:
                print("📊 Database already contains grant data, skipping seed")
                return True
            
            # Create sample grants
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
                ),
                Grant(
                    grant_id="EIC-2024-ACCELERATOR-003",
                    title="Deep Tech AI Startups Accelerator",
                    program="EIC Accelerator",
                    description="Supporting deep tech startups leveraging AI for breakthrough innovations. Focus on companies developing novel AI applications in robotics, autonomous systems, advanced materials, and quantum computing applications.",
                    synopsis="Deep tech AI: robotics, autonomous systems, quantum computing",
                    total_budget=15000000,
                    min_funding_amount=500000,
                    max_funding_amount=2500000,
                    deadline=datetime.now() + timedelta(days=90),
                    project_start_date=datetime.now() + timedelta(days=180),
                    project_end_date=datetime.now() + timedelta(days=180 + 1095),  # 3 years
                    project_duration_months=36,
                    eligible_countries=["ALL_EU"],
                    target_organizations=["SME", "Startup", "Deep Tech Company"],
                    keywords=["deep tech", "ai", "robotics", "autonomous systems", "quantum computing", "breakthrough innovation"],
                    technology_areas=["AI", "Robotics", "Quantum", "Deep Tech"],
                    industry_sectors=["Technology", "Research", "Innovation"],
                    url="https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en",
                    status=GrantStatus.OPEN,
                    source_system="eic_accelerator",
                    complexity_score=85.0
                ),
                Grant(
                    grant_id="EUREKA-2024-AI-005",
                    title="AI for Sustainable Energy Solutions",
                    program="Eureka",
                    description="International collaboration program supporting AI applications in renewable energy, smart grids, energy efficiency optimization, and sustainable energy storage solutions for SMEs across Europe.",
                    synopsis="Sustainable AI: renewable energy, smart grids, energy efficiency",
                    total_budget=8000000,
                    min_funding_amount=200000,
                    max_funding_amount=800000,
                    deadline=datetime.now() + timedelta(days=120),
                    project_start_date=datetime.now() + timedelta(days=210),
                    project_end_date=datetime.now() + timedelta(days=210 + 912),  # 2.5 years
                    project_duration_months=30,
                    eligible_countries=["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI", "NO", "CH"],
                    target_organizations=["SME", "Energy Company", "Technology Provider", "Research Institute"],
                    keywords=["sustainable energy", "ai", "renewable energy", "smart grids", "energy efficiency"],
                    technology_areas=["AI", "Energy", "Sustainability"],
                    industry_sectors=["Energy", "Technology", "Sustainability"],
                    url="https://www.eurekanetwork.org/",
                    status=GrantStatus.OPEN,
                    source_system="eureka",
                    complexity_score=75.0
                )
            ]
            
            # Add grants to session
            for grant in sample_grants:
                db.add(grant)
            
            # Commit the transaction
            await db.commit()
            
            print(f"✅ Seeded database with {len(sample_grants)} sample grants!")
            print(f"   🎯 Grants cover: Healthcare AI, Manufacturing 4.0, Environmental AI, Deep Tech, Energy AI")
            return True
            
        finally:
            await db.close()
            
    except Exception as e:
        print(f"❌ Database seeding failed: {e}")
        return False


async def main():
    """Main initialization function."""
    print("🚀 EU GRANTS MONITOR - DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Step 1: Test database connection
    print("\n📋 STEP 1: TEST DATABASE CONNECTION")
    print("-" * 40)
    if not test_database_connection():
        print("\n❌ Cannot connect to database. Please fix connection issues first.")
        print("\n🔧 Quick fixes to try:")
        print("   1. Wait 2-3 minutes for Supabase project to fully initialize")
        print("   2. Check your .env file for correct SUPABASE_DATABASE_URL")
        print("   3. Verify your Supabase project is running in the dashboard")
        sys.exit(1)
    
    # Step 2: Run migrations
    print("\n📋 STEP 2: CREATE DATABASE SCHEMA")
    print("-" * 40)
    if not run_migrations():
        print("\n❌ Database migration failed.")
        print("\n🔧 You can try running migrations manually:")
        print("   alembic upgrade head")
        sys.exit(1)
    
    # Step 3: Seed database
    print("\n📋 STEP 3: SEED WITH SAMPLE DATA")
    print("-" * 40)
    if not await seed_database():
        print("\n⚠️  Database seeding failed, but schema is created.")
        print("   You can add grants manually through the API later.")
    
    # Success!
    print(f"\n{'='*60}")
    print("🎉 DATABASE INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("\n✅ Your Supabase database is ready for the EU Grants Monitor!")
    print("\n🚀 Next steps:")
    print("   1. Start the backend server:")
    print("      uvicorn app.main:app --reload")
    print("   2. Visit: http://localhost:8000/docs for API documentation")
    print("   3. Check grants: http://localhost:8000/api/grants")
    
    print(f"\n🔗 Supabase Dashboard: {os.getenv('SUPABASE_URL', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
