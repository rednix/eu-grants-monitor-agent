#!/usr/bin/env python3
"""
Sync grants from core agent database to webapp database.

This script migrates grants from the core agent's SQLite database to the
webapp backend database, ensuring compatibility with the webapp models.
"""

import sqlite3
import json
import sys
import os
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Any

# Add webapp backend to path
webapp_backend_path = Path(__file__).parent / "webapp" / "backend"
sys.path.insert(0, str(webapp_backend_path))

try:
    from app.database import engine, SessionLocal, create_tables
    from app.models import Grant as WebappGrant, GrantStatus
    from sqlalchemy import text
except ImportError as e:
    print(f"Error importing webapp modules: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


def migrate_grants():
    """Migrate grants from core agent SQLite to webapp database."""
    
    # Paths
    core_agent_db = Path(__file__).parent / "data" / "grants.db"
    
    if not core_agent_db.exists():
        print(f"❌ Core agent database not found at: {core_agent_db}")
        return
    
    print(f"🔄 Syncing grants from {core_agent_db}")
    
    # Connect to core agent database
    core_conn = sqlite3.connect(str(core_agent_db))
    core_conn.row_factory = sqlite3.Row  # Enable column access by name
    
    # Connect to webapp database
    webapp_session = SessionLocal()
    
    try:
        # First, ensure webapp database tables exist
        print("🏗️ Creating webapp database tables...")
        # For SQLite, we need to handle the JSON columns differently
        try:
            webapp_session.execute(text("SELECT 1 FROM grants LIMIT 1"))
        except Exception:
            # Tables don't exist, create them
            from app.models import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Webapp database tables created")
        
        # Get grants from core agent database
        cursor = core_conn.cursor()
        cursor.execute("""
            SELECT * FROM grants 
            ORDER BY created_at DESC
        """)
        
        core_grants = cursor.fetchall()
        print(f"📊 Found {len(core_grants)} grants in core agent database")
        
        if not core_grants:
            print("ℹ️ No grants to sync")
            return
        
        migrated_count = 0
        updated_count = 0
        
        for grant_row in core_grants:
            try:
                # Parse JSON fields
                eligible_countries = json.loads(grant_row['eligible_countries']) if grant_row['eligible_countries'] else []
                target_organizations = json.loads(grant_row['target_organizations']) if grant_row['target_organizations'] else []
                keywords = json.loads(grant_row['keywords']) if grant_row['keywords'] else []
                technology_areas = json.loads(grant_row['technology_areas']) if grant_row['technology_areas'] else []
                industry_sectors = json.loads(grant_row['industry_sectors']) if grant_row['industry_sectors'] else []
                
                # Check if grant already exists
                existing = webapp_session.query(WebappGrant).filter(
                    WebappGrant.grant_id == grant_row['grant_id']
                ).first()
                
                if existing:
                    # Update existing grant
                    existing.title = grant_row['title']
                    existing.program = grant_row['program']
                    existing.description = grant_row['description']
                    existing.synopsis = grant_row['synopsis']
                    existing.total_budget = grant_row['total_budget']
                    existing.min_funding_amount = grant_row['min_funding_amount']
                    existing.max_funding_amount = grant_row['max_funding_amount']
                    existing.deadline = datetime.fromisoformat(grant_row['deadline'].replace('Z', '+00:00')) if grant_row['deadline'] else None
                    existing.eligible_countries = eligible_countries
                    existing.target_organizations = target_organizations
                    existing.keywords = keywords
                    existing.technology_areas = technology_areas
                    existing.industry_sectors = industry_sectors
                    existing.url = grant_row['url']
                    existing.documents_url = grant_row['documents_url']
                    existing.status = GrantStatus.OPEN
                    existing.complexity_score = grant_row['complexity_score']
                    existing.source_system = grant_row['source_system'] or 'grants_monitor_agent'
                    existing.updated_at = datetime.now()
                    
                    updated_count += 1
                    print(f"🔄 Updated: {grant_row['grant_id']}")
                    
                else:
                    # Create new grant
                    new_grant = WebappGrant(
                        grant_id=grant_row['grant_id'],
                        title=grant_row['title'],
                        program=grant_row['program'],
                        description=grant_row['description'],
                        synopsis=grant_row['synopsis'],
                        total_budget=grant_row['total_budget'],
                        funding_rate=grant_row.get('funding_rate', 70.0),
                        min_funding_amount=grant_row['min_funding_amount'],
                        max_funding_amount=grant_row['max_funding_amount'],
                        deadline=datetime.fromisoformat(grant_row['deadline'].replace('Z', '+00:00')) if grant_row['deadline'] else None,
                        eligible_countries=eligible_countries,
                        target_organizations=target_organizations,
                        keywords=keywords,
                        technology_areas=technology_areas,
                        industry_sectors=industry_sectors,
                        url=grant_row['url'],
                        documents_url=grant_row['documents_url'],
                        status=GrantStatus.OPEN,
                        complexity_score=grant_row['complexity_score'],
                        source_system=grant_row['source_system'] or 'grants_monitor_agent',
                        created_at=datetime.fromisoformat(grant_row['created_at'].replace('Z', '+00:00')) if grant_row['created_at'] else datetime.now(),
                        updated_at=datetime.now()
                    )
                    
                    webapp_session.add(new_grant)
                    migrated_count += 1
                    print(f"✅ Migrated: {grant_row['grant_id']}")
                
            except Exception as e:
                print(f"❌ Error processing grant {grant_row['grant_id']}: {e}")
                continue
        
        # Commit all changes
        webapp_session.commit()
        
        print(f"\n🎉 Migration completed!")
        print(f"   - New grants migrated: {migrated_count}")
        print(f"   - Existing grants updated: {updated_count}")
        print(f"   - Total grants processed: {len(core_grants)}")
        
        # Verify the migration
        total_webapp_grants = webapp_session.query(WebappGrant).count()
        print(f"   - Total grants in webapp database: {total_webapp_grants}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        webapp_session.rollback()
        raise
        
    finally:
        webapp_session.close()
        core_conn.close()


def verify_migration():
    """Verify that grants were migrated successfully."""
    webapp_session = SessionLocal()
    
    try:
        grants = webapp_session.query(WebappGrant).limit(5).all()
        
        print(f"\n🔍 Sample grants in webapp database:")
        for grant in grants:
            days_until = (grant.deadline - datetime.now()).days if grant.deadline else "N/A"
            print(f"   - {grant.grant_id}: {grant.title}")
            print(f"     Program: {grant.program}, Budget: €{grant.total_budget:,}")
            print(f"     Deadline: {grant.deadline}, Days left: {days_until}")
            print(f"     Keywords: {grant.keywords[:3] if grant.keywords else []}")
            print()
            
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
    finally:
        webapp_session.close()


if __name__ == "__main__":
    print("🚀 Starting grants database migration...")
    print("   Core Agent DB -> Webapp DB")
    print("=" * 50)
    
    try:
        migrate_grants()
        verify_migration()
        
        print("\n✅ Migration completed successfully!")
        print("   You can now view grants at http://localhost:3000/grants")
        
    except Exception as e:
        print(f"\n❌ Migration failed with error: {e}")
        sys.exit(1)
