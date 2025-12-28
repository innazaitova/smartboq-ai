"""
Auto-initialize database tables on startup
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def init_tables():
    """Create tables if they don't exist"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("DATABASE_URL not found in environment")
        return
    
    engine = create_engine(DATABASE_URL)
    
    sql = """
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        subscription_tier VARCHAR(50) DEFAULT 'trial',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Add subscription_tier column if it doesn't exist (for existing tables)
    DO $$ 
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='users' AND column_name='subscription_tier') THEN
            ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(50) DEFAULT 'trial';
        END IF;
    END $$;

    -- Projects table
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        project_name VARCHAR(255) NOT NULL,
        project_type VARCHAR(100),
        location VARCHAR(255),
        area_sqft DECIMAL,
        status VARCHAR(50) DEFAULT 'draft',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Drawings table
    CREATE TABLE IF NOT EXISTS drawings (
        id SERIAL PRIMARY KEY,
        project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
        file_name VARCHAR(255) NOT NULL,
        file_path VARCHAR(500) NOT NULL,
        file_type VARCHAR(50),
        file_size INTEGER,
        status VARCHAR(50) DEFAULT 'pending',
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Elements table
    CREATE TABLE IF NOT EXISTS elements (
        id SERIAL PRIMARY KEY,
        drawing_id INTEGER REFERENCES drawings(id) ON DELETE CASCADE,
        element_type VARCHAR(100),
        quantity DECIMAL,
        unit VARCHAR(50),
        dimensions TEXT,
        material VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
        print("✅ Database tables initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    init_tables()
