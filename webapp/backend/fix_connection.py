#!/usr/bin/env python3
"""
Connection Fixing Script for Supabase

This script tries multiple approaches to establish a working database connection:
1. Direct PostgreSQL connection (port 5432)
2. Connection pooling (port 6543)
3. Alternative connection parameters
4. Supabase REST API fallback for basic operations
"""

import os
import sys
import time
import asyncio
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


def test_direct_connection(database_url: str, timeout: int = 10) -> bool:
    """Test direct PostgreSQL connection."""
    try:
        from sqlalchemy import create_engine, text
        
        print(f"🔄 Testing direct connection (timeout: {timeout}s)...")
        
        engine = create_engine(
            database_url,
            pool_timeout=timeout,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": timeout,
                "options": "-c statement_timeout=10s"
            }
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1;"))
            result.fetchone()
            
        print(f"✅ Direct connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Direct connection failed: {str(e)[:100]}...")
        return False


def test_pooler_connection(base_url: str, password: str, timeout: int = 10) -> bool:
    """Test connection through Supabase pooler."""
    try:
        # Extract project reference from URL
        project_ref = base_url.split("@")[1].split(".supabase.co")[0]
        pooler_url = f"postgresql://postgres:{password}@{project_ref}.pooler.supabase.co:6543/postgres"
        
        print(f"🔄 Testing pooler connection (port 6543)...")
        
        from sqlalchemy import create_engine, text
        engine = create_engine(
            pooler_url,
            pool_timeout=timeout,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": timeout,
                "options": "-c statement_timeout=10s"
            }
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1;"))
            result.fetchone()
            
        print(f"✅ Pooler connection successful!")
        print(f"📝 Updated .env with pooler URL")
        
        # Update .env file to use pooler
        update_env_with_pooler_url(pooler_url)
        return True
        
    except Exception as e:
        print(f"❌ Pooler connection failed: {str(e)[:100]}...")
        return False


def test_alternative_params(base_url: str, timeout: int = 15) -> bool:
    """Test connection with alternative parameters."""
    try:
        print(f"🔄 Testing with alternative parameters...")
        
        from sqlalchemy import create_engine, text
        engine = create_engine(
            base_url,
            pool_timeout=timeout,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            connect_args={
                "connect_timeout": timeout,
                "options": "-c statement_timeout=30s -c tcp_keepalives_idle=600"
            }
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            row = result.fetchone()
            
        print(f"✅ Alternative connection successful!")
        print(f"   PostgreSQL: {row[0].split(' ')[1]}")
        return True
        
    except Exception as e:
        print(f"❌ Alternative connection failed: {str(e)[:100]}...")
        return False


def test_supabase_rest_setup() -> bool:
    """Set up tables using Supabase REST API as fallback."""
    try:
        from supabase import create_client
        
        url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not url or not service_key:
            print("❌ Missing Supabase URL or service key")
            return False
            
        print(f"🔄 Testing Supabase REST API setup...")
        
        client = create_client(url, service_key)
        
        # Try to create a simple table using SQL
        sql = """
        CREATE TABLE IF NOT EXISTS test_connection (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        
        result = client.rpc('exec_sql', {'sql': sql}).execute()
        
        # Clean up test table
        client.rpc('exec_sql', {'sql': 'DROP TABLE IF EXISTS test_connection;'}).execute()
        
        print(f"✅ Supabase REST API working!")
        return True
        
    except Exception as e:
        print(f"❌ Supabase REST API test failed: {str(e)[:100]}...")
        return False


def update_env_with_pooler_url(pooler_url: str):
    """Update .env file to use pooler URL."""
    try:
        env_path = ".env"
        
        # Read existing .env
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update the SUPABASE_DATABASE_URL line
        updated_lines = []
        for line in lines:
            if line.startswith("SUPABASE_DATABASE_URL="):
                updated_lines.append(f"SUPABASE_DATABASE_URL={pooler_url}\n")
            else:
                updated_lines.append(line)
        
        # Write back to .env
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
            
    except Exception as e:
        print(f"⚠️  Could not update .env file: {e}")


def create_schema_via_supabase_sql():
    """Create database schema using Supabase SQL editor (manual instructions)."""
    print(f"\n🛠️  MANUAL SCHEMA CREATION OPTION:")
    print(f"=" * 50)
    print(f"If direct connections keep failing, you can create the schema manually:")
    print(f"")
    print(f"1. Go to your Supabase Dashboard: {os.getenv('SUPABASE_URL')}")
    print(f"2. Click on 'SQL Editor' in the left sidebar")
    print(f"3. Copy and paste the SQL from: migrations/versions/001_initial_migration.py")
    print(f"4. Run the SQL to create all tables")
    print(f"")
    print(f"This will create the same database schema as the migration.")


def wait_for_project_ready(max_wait: int = 300) -> bool:
    """Wait for Supabase project to be fully ready."""
    print(f"⏳ Waiting for Supabase project to be fully ready (max {max_wait}s)...")
    
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            # Test if we can reach the API
            import requests
            response = requests.get(
                f"{os.getenv('SUPABASE_URL')}/rest/v1/",
                headers={"apikey": os.getenv('SUPABASE_ANON_KEY')},
                timeout=5
            )
            
            if response.status_code in [200, 401]:  # 401 is expected without auth
                print(f"✅ Project API is responding!")
                return True
                
        except Exception:
            pass
        
        print(f"   Still waiting... ({int(time.time() - start_time)}s elapsed)")
        time.sleep(10)
    
    print(f"⏰ Timeout waiting for project to be ready")
    return False


def main():
    """Main connection fixing function."""
    print("🔧 SUPABASE CONNECTION FIX")
    print("=" * 50)
    
    # Get database URL
    database_url = os.getenv("SUPABASE_DATABASE_URL")
    if not database_url:
        print("❌ SUPABASE_DATABASE_URL not found in environment")
        return False
    
    print(f"🎯 Target: {database_url.split('@')[1].split(':')[0]}")
    
    # Wait for project to be ready
    if not wait_for_project_ready():
        print("⚠️  Project might not be fully ready, but continuing...")
    
    # Method 1: Try direct connection with short timeout
    if test_direct_connection(database_url, timeout=5):
        print(f"\n🎉 SUCCESS: Direct connection works!")
        return True
    
    # Method 2: Try pooler connection
    password = database_url.split(':')[2].split('@')[0]
    if test_pooler_connection(database_url, password):
        print(f"\n🎉 SUCCESS: Pooler connection works!")
        return True
    
    # Method 3: Try with alternative parameters
    if test_alternative_params(database_url, timeout=15):
        print(f"\n🎉 SUCCESS: Alternative connection works!")
        return True
    
    # Method 4: Test if REST API works for basic operations
    if test_supabase_rest_setup():
        print(f"\n⚠️  PostgreSQL direct connection failed, but REST API works")
        print(f"   You can use Supabase client for basic operations")
        create_schema_via_supabase_sql()
        return False
    
    # All methods failed
    print(f"\n❌ ALL CONNECTION METHODS FAILED")
    print(f"=" * 50)
    print(f"🔧 Troubleshooting steps:")
    print(f"   1. Check if your Supabase project is paused/inactive")
    print(f"   2. Verify the database password in your dashboard")
    print(f"   3. Try again in 5-10 minutes (projects can take time to initialize)")
    print(f"   4. Check your network/firewall settings for port 5432")
    print(f"   5. Contact Supabase support if issues persist")
    
    create_schema_via_supabase_sql()
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
