"""
SQLAlchemy ORM Models
Database models for User, Project, Drawing, and Element entities
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """User account model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    subscription_tier = Column(String(50), default="trial", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', tier='{self.subscription_tier}')>"


class Project(Base):
    """Construction project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_name = Column(String(255), nullable=False)
    project_type = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    area_sqft = Column(Float, nullable=True)
    status = Column(String(50), default="created", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    drawings = relationship("Drawing", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.project_name}', status='{self.status}')>"


class Drawing(Base):
    """Drawing/blueprint file model"""
    __tablename__ = "drawings"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    drawing_type = Column(String(50), nullable=False)
    status = Column(String(50), default="uploaded", nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="drawings")
    elements = relationship("Element", back_populates="drawing", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Drawing(id={self.id}, file='{self.file_name}', status='{self.status}')>"


class Element(Base):
    """Construction element detected in drawing"""
    __tablename__ = "elements"
    
    id = Column(Integer, primary_key=True, index=True)
    drawing_id = Column(Integer, ForeignKey("drawings.id", ondelete="CASCADE"), nullable=False, index=True)
    element_type = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    dimensions = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    unit_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    drawing = relationship("Drawing", back_populates="elements")
    
    def __repr__(self):
        return f"<Element(id={self.id}, type='{self.element_type}', qty={self.quantity})>"


# Optional: Helper function to create all tables
def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)


# Optional: Helper function to drop all tables
def drop_tables(engine):
    """Drop all tables from the database"""
    Base.metadata.drop_all(bind=engine)
