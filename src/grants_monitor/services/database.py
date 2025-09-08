"""
Database service for the EU Grants Monitor Agent.

This module provides database connectivity and storage functionality
using the existing Supabase PostgreSQL database.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from supabase import create_client, Client
from loguru import logger
from dotenv import load_dotenv

from ..data.models import Grant

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"Loaded environment variables from {env_path}")


class DatabaseService:
    """Database service for storing monitoring results in Supabase."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize database service.
        
        Args:
            config: Database configuration dictionary
        """
        self.config = config or {}
        self.engine = None
        self.SessionLocal = None
        self.supabase_client = None
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Initialize database connection to Supabase."""
        try:
            # Try to get Supabase connection from webapp backend .env
            webapp_env_path = Path(__file__).parent.parent.parent.parent / "webapp" / "backend" / ".env"
            database_url = None
            
            if webapp_env_path.exists():
                # Load environment variables from webapp backend .env
                with open(webapp_env_path, 'r') as f:
                    for line in f:
                        if line.startswith('SUPABASE_DATABASE_URL='):
                            database_url = line.split('=', 1)[1].strip()
                            break
            
            # Prioritize config over environment variables
            db_config = self.config.get('database', {})
            if db_config.get('type') == 'sqlite':
                sqlite_path = db_config.get('sqlite', {}).get('path', 'data/grants.db')
                # Create data directory if it doesn't exist
                Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
                database_url = f"sqlite:///{sqlite_path}"
            
            # Fallback to environment variables only if no config
            elif not database_url or "your-project-ref" in database_url:
                database_url = os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL")
            
            # Final fallback
            if not database_url:
                if db_config.get('type') == 'postgresql':
                    pg_config = db_config.get('postgresql', {})
                    database_url = (
                        f"postgresql://{pg_config.get('username', 'postgres')}:"
                        f"{pg_config.get('password', '')}@"
                        f"{pg_config.get('host', 'localhost')}:"
                        f"{pg_config.get('port', 5432)}/"
                        f"{pg_config.get('database', 'grants_monitor')}"
                    )
                else:
                    # Use SQLite as fallback
                    sqlite_path = db_config.get('sqlite', {}).get('path', 'data/grants.db')
                    # Create data directory if it doesn't exist
                    Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
                    database_url = f"sqlite:///{sqlite_path}"
            
            if not database_url:
                raise ValueError("No database configuration found")
            
            # Create engine with appropriate settings
            if database_url.startswith("postgresql"):
                self.engine = create_engine(
                    database_url,
                    pool_pre_ping=True,
                    pool_size=5,
                    max_overflow=10,
                    pool_recycle=1800,
                    echo=False
                )
                logger.info("Connected to PostgreSQL/Supabase database")
            else:
                self.engine = create_engine(
                    database_url,
                    connect_args={"check_same_thread": False},
                    echo=False
                )
                logger.info("Connected to SQLite database")
            
            # Create session maker
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Initialize database tables if using SQLite
            if database_url.startswith("sqlite"):
                self._initialize_sqlite_tables()
            
            # Initialize Supabase client for REST API operations
            self._initialize_supabase_client()
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise
    
    def _initialize_supabase_client(self) -> None:
        """Initialize Supabase client for REST API operations."""
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if supabase_url and supabase_service_key:
                self.supabase_client = create_client(supabase_url, supabase_service_key)
                logger.info("Supabase client initialized")
            else:
                logger.warning("Supabase URL or service key not found, client not initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
    
    def _initialize_sqlite_tables(self) -> None:
        """Initialize SQLite database tables."""
        create_grants_table = """
        CREATE TABLE IF NOT EXISTS grants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grant_id VARCHAR(255) UNIQUE NOT NULL,
            title VARCHAR(500) NOT NULL,
            program VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            synopsis TEXT,
            total_budget INTEGER NOT NULL,
            funding_rate FLOAT DEFAULT 70.0,
            min_funding_amount INTEGER,
            max_funding_amount INTEGER,
            deadline DATETIME NOT NULL,
            project_start_date DATETIME,
            project_end_date DATETIME,
            project_duration_months INTEGER,
            eligible_countries TEXT,
            target_organizations TEXT,
            keywords TEXT,
            technology_areas TEXT,
            industry_sectors TEXT,
            url VARCHAR(500),
            documents_url VARCHAR(500),
            status VARCHAR(50) DEFAULT 'open',
            complexity_score FLOAT,
            source_system VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        try:
            with self.get_session() as session:
                session.execute(text(create_grants_table))
                session.commit()
                logger.info("SQLite database tables initialized")
        except Exception as e:
            logger.error(f"Error initializing SQLite tables: {e}")
    
    def get_session(self) -> Session:
        """Get a database session.
        
        Returns:
            Database session
        """
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized")
        return self.SessionLocal()
    
    def test_connection(self) -> bool:
        """Test database connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        # First try Supabase client if available
        if self.supabase_client:
            try:
                # Test by querying grants table
                result = self.supabase_client.table('grants').select('grant_id').limit(1).execute()
                logger.info("Supabase client connection test successful")
                return True
            except Exception as e:
                logger.warning(f"Supabase client connection test failed: {e}")
        
        # Fallback to SQLAlchemy connection
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def store_grants(self, grants: List[Grant]) -> None:
        """Store grants in the database.
        
        Args:
            grants: List of grants to store
        """
        if not grants:
            logger.info("No grants to store")
            return
        
        # First try Supabase client if available
        if self.supabase_client:
            try:
                return self._store_grants_via_supabase(grants)
            except Exception as e:
                logger.warning(f"Supabase client storage failed, falling back to SQLAlchemy: {e}")
        
        # Fallback to SQLAlchemy
        try:
            with self.get_session() as session:
                stored_count = 0
                updated_count = 0
                
                for grant in grants:
                    try:
                        # Check if grant already exists
                        existing_grant = session.execute(
                            text("SELECT id FROM grants WHERE grant_id = :grant_id"),
                            {"grant_id": grant.id}
                        ).fetchone()
                        
                        if existing_grant:
                            # Update existing grant
                            self._update_grant_in_db(session, grant)
                            updated_count += 1
                        else:
                            # Insert new grant
                            self._insert_grant_to_db(session, grant)
                            stored_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error storing grant {grant.id}: {e}")
                        continue
                
                session.commit()
                logger.info(f"Database storage complete: {stored_count} new grants, {updated_count} updated")
                
        except SQLAlchemyError as e:
            logger.error(f"Database error storing grants: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error storing grants: {e}")
            raise
    
    def _store_grants_via_supabase(self, grants: List[Grant]) -> None:
        """Store grants using Supabase client.
        
        Args:
            grants: List of grants to store
        """
        stored_count = 0
        updated_count = 0
        
        for grant in grants:
            try:
                # Convert grant to database format
                grant_data = {
                    'grant_id': grant.id,
                    'title': grant.title,
                    'program': grant.program.value if hasattr(grant.program, 'value') else str(grant.program),
                    'description': grant.description,
                    'synopsis': grant.synopsis or grant.description[:200] + '...',
                    'total_budget': int(grant.funding_amount),
                    'funding_rate': 70.0,
                    'min_funding_amount': int(grant.min_funding) if grant.min_funding else None,
                    'max_funding_amount': int(grant.max_funding) if grant.max_funding else None,
                    'deadline': grant.deadline.isoformat() if grant.deadline else None,
                    'eligible_countries': grant.eligible_countries,
                    'target_organizations': grant.target_organizations,
                    'keywords': grant.keywords,
                    'technology_areas': getattr(grant, 'technology_areas', []),
                    'industry_sectors': getattr(grant, 'industry_sectors', []),
                    'url': grant.url,
                    'documents_url': getattr(grant, 'documents_url', None),
                    'status': 'open',
                    'complexity_score': grant.complexity_score,
                    'source_system': 'grants_monitor_agent',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                # Try to upsert (insert or update)
                result = self.supabase_client.table('grants').upsert(grant_data, on_conflict='grant_id').execute()
                
                if result.data:
                    # Check if it was an insert or update based on the response
                    if len(result.data) > 0:
                        stored_count += 1
                
            except Exception as e:
                logger.error(f"Error storing grant {grant.id} via Supabase: {e}")
                continue
        
        logger.info(f"Supabase storage complete: {stored_count} grants processed")
    
    def _insert_grant_to_db(self, session: Session, grant: Grant) -> None:
        """Insert a new grant into the database.
        
        Args:
            session: Database session
            grant: Grant to insert
        """
        # Convert Grant model to database format
        grant_data = {
            'grant_id': grant.id,
            'title': grant.title,
            'program': grant.program.value,
            'description': grant.description,
            'synopsis': grant.synopsis,
            'total_budget': int(grant.funding_amount),
            'min_funding_amount': grant.min_funding,
            'max_funding_amount': grant.max_funding,
            'deadline': grant.deadline,
            'eligible_countries': json.dumps(grant.eligible_countries),
            'target_organizations': json.dumps(grant.target_organizations),
            'keywords': json.dumps(grant.keywords),
            'technology_areas': json.dumps(getattr(grant, 'technology_areas', [])),
            'industry_sectors': json.dumps(getattr(grant, 'industry_sectors', [])),
            'url': grant.url,
            'documents_url': getattr(grant, 'documents_url', None),
            'status': 'open',
            'complexity_score': grant.complexity_score,
            'source_system': 'grants_monitor_agent',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # Build INSERT query
        columns = ', '.join(grant_data.keys())
        placeholders = ', '.join(f':{key}' for key in grant_data.keys())
        query = f"INSERT INTO grants ({columns}) VALUES ({placeholders})"
        
        session.execute(text(query), grant_data)
    
    def _update_grant_in_db(self, session: Session, grant: Grant) -> None:
        """Update an existing grant in the database.
        
        Args:
            session: Database session
            grant: Grant to update
        """
        # Update relevant fields
        grant_data = {
            'grant_id': grant.id,
            'title': grant.title,
            'description': grant.description,
            'synopsis': grant.synopsis,
            'total_budget': int(grant.funding_amount),
            'complexity_score': grant.complexity_score,
            'keywords': json.dumps(grant.keywords),
            'updated_at': datetime.now()
        }
        
        query = """
            UPDATE grants SET 
                title = :title,
                description = :description,
                synopsis = :synopsis,
                total_budget = :total_budget,
                complexity_score = :complexity_score,
                keywords = :keywords,
                updated_at = :updated_at
            WHERE grant_id = :grant_id
        """
        
        session.execute(text(query), grant_data)
    
    def store_monitoring_session(self, session_data: Dict[str, Any]) -> str:
        """Store monitoring session data.
        
        Args:
            session_data: Session data to store
            
        Returns:
            Session ID
        """
        try:
            with self.get_session() as session:
                session_id = f"monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # For now, just log the session (you could create a monitoring_sessions table)
                logger.info(f"Monitoring session {session_id}: {session_data}")
                
                return session_id
                
        except Exception as e:
            logger.error(f"Error storing monitoring session: {e}")
            raise
    
    def get_grants_by_program(self, program: str) -> List[Dict[str, Any]]:
        """Get grants by program.
        
        Args:
            program: Program name
            
        Returns:
            List of grants
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("SELECT * FROM grants WHERE program = :program ORDER BY deadline"),
                    {"program": program}
                ).fetchall()
                
                return [dict(row._mapping) for row in result]
                
        except Exception as e:
            logger.error(f"Error fetching grants by program: {e}")
            return []
    
    def close(self) -> None:
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
