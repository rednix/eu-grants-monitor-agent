#!/usr/bin/env python3
"""
Alternative setup script using Supabase REST API.

This script works around PostgreSQL connection issues by using
the Supabase REST API to verify the database setup.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_api_connection():
    """Check if Supabase API is accessible."""
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY")
            return False
        
        print(f"🔄 Testing Supabase API connection...")
        
        response = requests.get(
            f"{url}/rest/v1/",
            headers={
                "apikey": key,
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code in [200, 401]:  # 401 is expected without proper auth
            print(f"✅ Supabase API is accessible!")
            return True
        else:
            print(f"❌ API returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False


def check_tables_exist():
    """Check if our tables exist via REST API."""
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        tables_to_check = ["grants", "users", "companies", "applications", "payment_transactions"]
        existing_tables = []
        
        print(f"🔄 Checking for existing tables...")
        
        for table in tables_to_check:
            try:
                response = requests.get(
                    f"{url}/rest/v1/{table}?limit=1",
                    headers={
                        "apikey": key,
                        "Content-Type": "application/json"
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    existing_tables.append(table)
                    
            except Exception:
                continue
        
        if existing_tables:
            print(f"✅ Found existing tables: {', '.join(existing_tables)}")
            return existing_tables
        else:
            print(f"⚠️  No tables found - schema needs to be created")
            return []
            
    except Exception as e:
        print(f"❌ Table check failed: {e}")
        return []


def check_sample_data():
    """Check if we have sample grant data."""
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        print(f"🔄 Checking for sample data...")
        
        response = requests.get(
            f"{url}/rest/v1/grants?select=grant_id,title&limit=10",
            headers={
                "apikey": key,
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            grants = response.json()
            if grants:
                print(f"✅ Found {len(grants)} sample grants:")
                for grant in grants[:3]:  # Show first 3
                    print(f"   • {grant['grant_id']}: {grant['title'][:50]}...")
                if len(grants) > 3:
                    print(f"   ... and {len(grants) - 3} more")
                return True
            else:
                print(f"⚠️  No sample grants found")
                return False
        else:
            print(f"⚠️  Could not check grants (status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Sample data check failed: {e}")
        return False


def generate_setup_instructions():
    """Generate step-by-step setup instructions."""
    
    dashboard_url = os.getenv("SUPABASE_URL")
    
    instructions = f"""
🛠️  MANUAL SETUP INSTRUCTIONS
{'='*60}

Since direct PostgreSQL connections are not working, please set up
the database manually through the Supabase Dashboard:

📋 STEP 1: OPEN SUPABASE DASHBOARD
   🔗 {dashboard_url}

📋 STEP 2: CREATE DATABASE SCHEMA
   1. Click "SQL Editor" in the left sidebar
   2. Click "New Query" 
   3. Copy the entire content from: schema.sql
   4. Paste it into the editor
   5. Click "Run" to execute

📋 STEP 3: VERIFY SETUP
   1. Click "Table Editor" in the left sidebar
   2. You should see these tables:
      • users
      • companies  
      • grants
      • applications
      • payment_transactions
   
   3. Click on "grants" table
   4. You should see 5 sample grants

📋 STEP 4: TEST API ACCESS
   Run this script again to verify everything works:
   python setup_via_api.py

🎯 WHAT THE SCHEMA INCLUDES:
   ✅ Complete database structure for EU Grants Monitor
   ✅ 5 sample EU grants (Healthcare AI, Manufacturing, etc.)
   ✅ Row Level Security (RLS) policies
   ✅ Proper indexes for performance
   ✅ JSON fields for flexible data storage

🔐 SECURITY FEATURES:
   • Users can only see their own data
   • Company data is private to company members  
   • Grants are publicly readable
   • Payment data is private to users
   • All tables have Row Level Security enabled

Once this is done, you can start the backend server with:
   uvicorn app.main:app --reload
"""
    
    return instructions


def test_backend_compatibility():
    """Test if the backend can work with current setup."""
    try:
        print(f"🔄 Testing backend compatibility...")
        
        # Try importing our models
        from app.models import Grant, User, Company
        print(f"✅ Models imported successfully")
        
        # Try importing database setup
        from app.database import SUPABASE_URL, SUPABASE_ANON_KEY
        if SUPABASE_URL and SUPABASE_ANON_KEY:
            print(f"✅ Database configuration loaded")
        else:
            print(f"⚠️  Some database config missing")
        
        # Try importing config
        from app.config import settings
        print(f"✅ Application config loaded")
        
        print(f"✅ Backend should work with current setup!")
        return True
        
    except Exception as e:
        print(f"❌ Backend compatibility issue: {e}")
        return False


def main():
    """Main setup verification function."""
    print("🔧 EU GRANTS MONITOR - API-BASED SETUP CHECK")
    print("=" * 60)
    
    # Step 1: Check API connection
    print("\n📋 STEP 1: SUPABASE API CONNECTION")
    print("-" * 40)
    if not check_api_connection():
        print("\n❌ Cannot access Supabase API")
        print("   Check your SUPABASE_URL and SUPABASE_ANON_KEY in .env")
        return False
    
    # Step 2: Check if tables exist
    print("\n📋 STEP 2: DATABASE TABLES")
    print("-" * 40)
    existing_tables = check_tables_exist()
    
    if len(existing_tables) >= 3:  # At least grants, users, companies
        print("✅ Database schema appears to be set up!")
        schema_ready = True
    else:
        print("⚠️  Database schema needs to be created")
        schema_ready = False
    
    # Step 3: Check sample data
    print("\n📋 STEP 3: SAMPLE DATA")
    print("-" * 40)
    has_data = check_sample_data()
    
    # Step 4: Test backend compatibility
    print("\n📋 STEP 4: BACKEND COMPATIBILITY")
    print("-" * 40)
    backend_ok = test_backend_compatibility()
    
    # Summary and next steps
    print(f"\n{'='*60}")
    print("📊 SETUP STATUS SUMMARY")
    print("=" * 60)
    print(f"   API Connection:      {'✅ OK' if True else '❌ Failed'}")
    print(f"   Database Schema:     {'✅ OK' if schema_ready else '⚠️  Missing'}")
    print(f"   Sample Data:         {'✅ OK' if has_data else '⚠️  Missing'}")
    print(f"   Backend Ready:       {'✅ OK' if backend_ok else '❌ Issues'}")
    
    if schema_ready and has_data and backend_ok:
        print(f"\n🎉 SETUP COMPLETE!")
        print(f"✅ Your database is ready for the EU Grants Monitor")
        print(f"\n🚀 Start the backend server:")
        print(f"   uvicorn app.main:app --reload")
        print(f"\n📊 API endpoints will be available at:")
        print(f"   http://localhost:8000/docs")
        print(f"   http://localhost:8000/api/grants")
        return True
    else:
        print(f"\n⚠️  MANUAL SETUP REQUIRED")
        print(generate_setup_instructions())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
