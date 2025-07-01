"""SQLAlchemy V2 database setup"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from app.core.config import settings
from app.core.logging import app_logger

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        app_logger.info("Database tables created successfully")
    except Exception as e:
        app_logger.error(f"Error creating database tables: {e}")
        raise

def get_db() -> Session:
    """Database session dependency."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()