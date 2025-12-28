"""
Database Connection & Models
SQLAlchemy setup and database utilities
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/quantibot"
)

# Create engine with shorter timeout
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={'connect_timeout': 5},
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions
    
    Usage:
        with get_db_context() as db:
            # Use db session
            pass
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database (create all tables)"""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)


# Database utilities
class DatabaseUtils:
    """Utility functions for database operations"""
    
    @staticmethod
    def execute_raw_sql(query: str, params: dict = None):
        """Execute raw SQL query"""
        with get_db_context() as db:
            result = db.execute(query, params or {})
            return result.fetchall()
    
    @staticmethod
    def backup_database(backup_path: str):
        """Create database backup"""
        import subprocess
        
        db_name = os.getenv("DB_NAME", "quantibot")
        db_user = os.getenv("DB_USER", "postgres")
        
        command = f"pg_dump -U {db_user} {db_name} > {backup_path}"
        subprocess.run(command, shell=True, check=True)
    
    @staticmethod
    def restore_database(backup_path: str):
        """Restore database from backup"""
        import subprocess
        
        db_name = os.getenv("DB_NAME", "quantibot")
        db_user = os.getenv("DB_USER", "postgres")
        
        command = f"psql -U {db_user} {db_name} < {backup_path}"
        subprocess.run(command, shell=True, check=True)
