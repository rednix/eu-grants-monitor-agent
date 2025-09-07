"""
Alternative database configurations for different providers.

This file shows how to configure the application for:
1. Supabase (PostgreSQL-as-a-Service)
2. MySQL 
3. SQLite (development)
"""

from sqlalchemy import create_engine, Text, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects import mysql, postgresql
import os
from typing import AsyncGenerator

from .config import settings


# =============================================================================
# SUPABASE CONFIGURATION (PostgreSQL-as-a-Service)
# =============================================================================

def setup_supabase_database():
    """
    Configure for Supabase - PostgreSQL-as-a-Service
    
    Advantages:
    - Managed PostgreSQL with built-in auth
    - Real-time subscriptions
    - Built-in API generation
    - Free tier: 500MB storage, 50MB file uploads
    - Automatic backups and scaling
    """
    
    # Supabase connection URL format:
    # postgresql://postgres:[PASSWORD]@[PROJECT_REF].supabase.co:5432/postgres
    
    supabase_url = os.getenv(
        "SUPABASE_DATABASE_URL",
        "postgresql://postgres:your-password@your-project.supabase.co:5432/postgres"
    )
    
    engine = create_engine(
        supabase_url,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )
    
    # Async engine for Supabase
    async_supabase_url = supabase_url.replace("postgresql://", "postgresql+asyncpg://")
    async_engine = create_async_engine(
        async_supabase_url,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )
    
    return engine, async_engine


# =============================================================================
# MYSQL CONFIGURATION
# =============================================================================

def setup_mysql_database():
    """
    Configure for MySQL
    
    Advantages:
    - Widespread hosting support
    - Lower cost options
    - Familiar to many developers
    - Good performance for read-heavy workloads
    
    Note: MySQL has limited JSON support compared to PostgreSQL
    """
    
    mysql_url = os.getenv(
        "MYSQL_DATABASE_URL",
        "mysql+pymysql://user:password@localhost:3306/eu_grants_monitor"
    )
    
    engine = create_engine(
        mysql_url,
        pool_pre_ping=True,
        echo=settings.DEBUG,
        # MySQL-specific settings
        pool_size=20,
        max_overflow=0,
        pool_recycle=3600
    )
    
    # MySQL doesn't have great async support, so we'll use sync only
    async_engine = None
    
    return engine, async_engine


# =============================================================================
# SQLITE CONFIGURATION (Development/Small Deployments)
# =============================================================================

def setup_sqlite_database():
    """
    Configure for SQLite
    
    Advantages:
    - Zero configuration
    - Perfect for development
    - Single file database
    - No server required
    
    Disadvantages:
    - Limited JSON support
    - No concurrent writes
    - Not suitable for production with multiple users
    """
    
    sqlite_url = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./eu_grants_monitor.db")
    
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
    
    # SQLite doesn't support async in our setup
    async_engine = None
    
    return engine, async_engine


# =============================================================================
# MODEL ADAPTATIONS FOR DIFFERENT DATABASES
# =============================================================================

def get_json_column_type():
    """
    Return appropriate JSON column type based on database.
    """
    db_url = settings.DATABASE_URL.lower()
    
    if 'mysql' in db_url:
        # MySQL 5.7+ supports JSON, earlier versions need TEXT
        return mysql.JSON()
    elif 'sqlite' in db_url:
        # SQLite stores JSON as TEXT
        return Text()
    else:
        # PostgreSQL (including Supabase)
        return postgresql.JSON()


def get_array_column_type():
    """
    Handle array fields for different databases.
    
    PostgreSQL has native arrays, others need workarounds.
    """
    db_url = settings.DATABASE_URL.lower()
    
    if 'postgresql' in db_url or 'supabase' in db_url:
        # PostgreSQL native arrays
        from sqlalchemy.dialects.postgresql import ARRAY
        return ARRAY(String)
    else:
        # For MySQL/SQLite, store arrays as JSON
        return get_json_column_type()


# =============================================================================
# ENVIRONMENT-SPECIFIC SETUP
# =============================================================================

def get_database_engines():
    """
    Get database engines based on environment configuration.
    """
    db_url = settings.DATABASE_URL.lower()
    
    if 'supabase.co' in db_url:
        print("🟢 Using Supabase (PostgreSQL-as-a-Service)")
        return setup_supabase_database()
    
    elif 'mysql' in db_url:
        print("🟡 Using MySQL")
        return setup_mysql_database()
    
    elif 'sqlite' in db_url:
        print("🔵 Using SQLite (Development)")
        return setup_sqlite_database()
    
    elif 'postgresql' in db_url:
        print("🟣 Using PostgreSQL")
        # Use original PostgreSQL setup
        from .database import engine, async_engine
        return engine, async_engine
    
    else:
        print("⚠️ Unknown database type, defaulting to SQLite")
        return setup_sqlite_database()


# =============================================================================
# SUPABASE-SPECIFIC FEATURES
# =============================================================================

class SupabaseIntegration:
    """
    Additional Supabase features integration.
    """
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
    
    def setup_realtime_subscriptions(self):
        """
        Set up real-time subscriptions for grant updates.
        """
        # This would integrate with Supabase real-time features
        # to notify users when new grants are added
        pass
    
    def setup_row_level_security(self):
        """
        Configure Row Level Security policies.
        """
        policies = [
            # Users can only see their own data
            "CREATE POLICY user_data ON users FOR ALL USING (auth.uid() = id)",
            
            # Companies can be seen by their members
            "CREATE POLICY company_access ON companies FOR ALL USING (auth.uid() IN (SELECT user_id FROM users WHERE company_id = companies.id))",
            
            # Grants are public for reading
            "CREATE POLICY grants_public ON grants FOR SELECT USING (true)",
        ]
        return policies
    
    def setup_storage_buckets(self):
        """
        Set up storage buckets for uploaded documents.
        """
        buckets = [
            {
                "name": "application_documents",
                "public": False,
                "file_size_limit": 10485760,  # 10MB
                "allowed_mime_types": ["application/pdf", "image/jpeg", "image/png"]
            }
        ]
        return buckets


# =============================================================================
# MYSQL-SPECIFIC OPTIMIZATIONS
# =============================================================================

class MySQLOptimizations:
    """
    MySQL-specific optimizations and configurations.
    """
    
    @staticmethod
    def get_mysql_indexes():
        """
        MySQL-specific indexes for better performance.
        """
        return [
            "CREATE INDEX idx_grants_deadline ON grants(deadline)",
            "CREATE INDEX idx_grants_program ON grants(program)",
            "CREATE INDEX idx_grants_funding_amount ON grants(total_budget)",
            "CREATE FULLTEXT INDEX idx_grants_search ON grants(title, description)",
            "CREATE INDEX idx_users_email ON users(email)",
            "CREATE INDEX idx_applications_status ON applications(status)",
        ]
    
    @staticmethod
    def handle_json_arrays(data_list):
        """
        Convert Python lists to JSON strings for MySQL storage.
        """
        import json
        return json.dumps(data_list) if data_list else "[]"
    
    @staticmethod
    def parse_json_arrays(json_string):
        """
        Parse JSON strings back to Python lists from MySQL.
        """
        import json
        try:
            return json.loads(json_string) if json_string else []
        except json.JSONDecodeError:
            return []


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

"""
SUPABASE SETUP:
--------------

1. Create Supabase project at https://supabase.com
2. Get your database URL and API key
3. Set environment variables:
   
   SUPABASE_DATABASE_URL=postgresql://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres
   SUPABASE_URL=https://[PROJECT].supabase.co
   SUPABASE_ANON_KEY=your_anon_key

4. Update main application:
   from .database_alternatives import get_database_engines
   engine, async_engine = get_database_engines()

MYSQL SETUP:
-----------

1. Install MySQL server or use managed service (AWS RDS, Google Cloud SQL)
2. Install MySQL driver: pip install pymysql
3. Set environment variable:
   
   MYSQL_DATABASE_URL=mysql+pymysql://user:password@localhost:3306/eu_grants_monitor

4. Use MySQL-specific model adaptations for JSON fields

SQLITE SETUP (Development):
--------------------------

1. No installation required
2. Set environment variable:
   
   SQLITE_DATABASE_URL=sqlite:///./eu_grants_monitor.db

3. Perfect for development and testing
"""
