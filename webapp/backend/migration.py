"""
Quick migration script to add hashed_password column to users table.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def add_hashed_password_column():
    """Add hashed_password column to users table."""
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DATABASE_URL")
    if not database_url:
        print("DATABASE_URL or SUPABASE_DATABASE_URL environment variable not set")
        return False
    
    try:
        # Connect to the database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'hashed_password'
        """)
        
        if cursor.fetchone():
            print("hashed_password column already exists")
            return True
        
        # Add the column if it doesn't exist
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255) NULL
        """)
        
        conn.commit()
        print("Successfully added hashed_password column to users table")
        return True
        
    except Exception as e:
        print(f"Error adding hashed_password column: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    add_hashed_password_column()
