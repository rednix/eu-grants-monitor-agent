#!/usr/bin/env python3
"""
Test Supabase database connection.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test sync connection
def test_sync_connection():
    """Test synchronous database connection."""
    try:
        from sqlalchemy import create_engine, text
        
        database_url = os.getenv("SUPABASE_DATABASE_URL")
        if not database_url:
            print("❌ SUPABASE_DATABASE_URL not found in environment")
            return False
            
        print(f"🔄 Testing sync connection to: {database_url.split('@')[1].split(':')[0]}")
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version(), current_database(), current_user;"))
            row = result.fetchone()
            
        print(f"✅ Sync connection successful!")
        print(f"   PostgreSQL Version: {row[0].split(' ')[1]}")
        print(f"   Database: {row[1]}")
        print(f"   User: {row[2]}")
        return True
        
    except Exception as e:
        print(f"❌ Sync connection failed: {e}")
        return False


# Test async connection
async def test_async_connection():
    """Test asynchronous database connection."""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        database_url = os.getenv("SUPABASE_DATABASE_URL")
        async_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        
        print(f"🔄 Testing async connection...")
        
        async_engine = create_async_engine(async_url)
        
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SELECT version(), current_database(), current_user;"))
            row = result.fetchone()
            
        print(f"✅ Async connection successful!")
        print(f"   PostgreSQL Version: {row[0].split(' ')[1]}")
        print(f"   Database: {row[1]}")
        print(f"   User: {row[2]}")
        return True
        
    except Exception as e:
        print(f"❌ Async connection failed: {e}")
        return False


# Test Supabase client
def test_supabase_client():
    """Test Supabase Python client."""
    try:
        from supabase import create_client, Client
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ Supabase URL or API key not found")
            return False
            
        print(f"🔄 Testing Supabase client...")
        
        supabase: Client = create_client(url, key)
        
        # Test a simple query (this will fail if no tables exist, but confirms connection)
        try:
            # Try to query system tables instead
            result = supabase.rpc('version').execute()
            print(f"✅ Supabase client connection successful!")
            return True
        except Exception as client_error:
            # Even if the query fails, if we get a proper API response, connection is working
            if "does not exist" in str(client_error) or "permission denied" in str(client_error):
                print(f"✅ Supabase client connection successful! (expected error for empty database)")
                return True
            else:
                raise client_error
        
    except Exception as e:
        print(f"❌ Supabase client failed: {e}")
        return False


def main():
    """Main test function."""
    print("🟢 SUPABASE CONNECTION TEST")
    print("=" * 40)
    
    # Test 1: Sync connection
    print("\n1. Testing synchronous connection:")
    sync_ok = test_sync_connection()
    
    # Test 2: Async connection  
    print("\n2. Testing asynchronous connection:")
    import asyncio
    async_ok = asyncio.run(test_async_connection())
    
    # Test 3: Supabase client
    print("\n3. Testing Supabase Python client:")
    client_ok = test_supabase_client()
    
    # Summary
    print(f"\n{'='*40}")
    print("🎯 TEST RESULTS:")
    print(f"   Sync Connection:     {'✅ OK' if sync_ok else '❌ Failed'}")
    print(f"   Async Connection:    {'✅ OK' if async_ok else '❌ Failed'}")
    print(f"   Supabase Client:     {'✅ OK' if client_ok else '❌ Failed'}")
    
    if sync_ok and async_ok:
        print(f"\n🎉 All database connections working!")
        print("✅ Your Supabase setup is ready for the EU Grants Monitor!")
        return True
    else:
        print(f"\n⚠️  Some connections failed. Please check:")
        print("   1. Supabase project is fully initialized (can take 2-5 minutes)")
        print("   2. Database password is correct")
        print("   3. No firewall blocking the connection")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
