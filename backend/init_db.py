"""
Database Initialization Script
Creates the PostgreSQL database and tables
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'quantibot')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'yourpassword')

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"✓ Database '{DB_NAME}' created successfully")
        else:
            print(f"✓ Database '{DB_NAME}' already exists")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False

def create_tables():
    """Create tables in the database"""
    try:
        # Connect to the quantibot database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Read and execute schema file
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database_schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        
        print(f"✓ Tables created successfully in '{DB_NAME}'")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def main():
    print("=" * 60)
    print("QuantiBot AI - Database Initialization")
    print("=" * 60)
    print()
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        print("\n⚠ Failed to create database. Please check:")
        print("  - PostgreSQL is running")
        print(f"  - User '{DB_USER}' has CREATE DATABASE permission")
        print(f"  - Password in .env file is correct")
        return
    print()
    
    # Step 2: Create tables
    print("Step 2: Creating tables...")
    if not create_tables():
        print("\n⚠ Failed to create tables. Check the error above.")
        return
    print()
    
    print("=" * 60)
    print("✓ Database initialization completed successfully!")
    print("=" * 60)
    print()
    print("You can now start the application:")
    print("  uvicorn main:app --reload --port 8000")
    print()

if __name__ == "__main__":
    main()
