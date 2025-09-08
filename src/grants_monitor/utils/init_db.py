"""
Database initialization utilities.

This module provides functions to initialize the database schema.
"""

from sqlalchemy import create_engine, text
from loguru import logger
import os
from pathlib import Path


def create_sqlite_tables(database_url: str) -> None:
    """Create SQLite database tables."""
    engine = create_engine(database_url)
    
    # Create grants table compatible with webapp backend schema
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
        eligible_countries TEXT,  -- JSON as TEXT in SQLite
        target_organizations TEXT,  -- JSON as TEXT in SQLite
        keywords TEXT,  -- JSON as TEXT in SQLite
        technology_areas TEXT,  -- JSON as TEXT in SQLite
        industry_sectors TEXT,  -- JSON as TEXT in SQLite
        url VARCHAR(500),
        documents_url VARCHAR(500),
        status VARCHAR(50) DEFAULT 'open',
        complexity_score FLOAT,
        source_system VARCHAR(100),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Create index for better performance
    create_indexes = [
        "CREATE INDEX IF NOT EXISTS idx_grants_grant_id ON grants(grant_id)",
        "CREATE INDEX IF NOT EXISTS idx_grants_program ON grants(program)",
        "CREATE INDEX IF NOT EXISTS idx_grants_deadline ON grants(deadline)",
        "CREATE INDEX IF NOT EXISTS idx_grants_status ON grants(status)"
    ]
    
    try:
        with engine.connect() as conn:
            # Create table
            conn.execute(text(create_grants_table))
            
            # Create indexes
            for index_sql in create_indexes:
                conn.execute(text(index_sql))
            
            conn.commit()
            logger.info("✅ SQLite database tables created successfully")
    
    except Exception as e:
        logger.error(f"❌ Error creating SQLite tables: {e}")
        raise
    finally:
        engine.dispose()


def init_database(config: dict) -> None:
    """Initialize database based on configuration."""
    db_config = config.get('database', {})
    db_type = db_config.get('type', 'sqlite')
    
    if db_type == 'sqlite':
        sqlite_path = db_config.get('sqlite', {}).get('path', 'data/grants.db')
        # Ensure data directory exists
        Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        database_url = f"sqlite:///{sqlite_path}"
        create_sqlite_tables(database_url)
    else:
        logger.info("PostgreSQL/Supabase tables should be managed through webapp backend migrations")


if __name__ == "__main__":
    # Can be run directly to initialize database
    from ..utils.config import ConfigManager
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    init_database(config)
