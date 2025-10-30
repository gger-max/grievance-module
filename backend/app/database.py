import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Configure engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,  # Use NullPool for SQLite to avoid threading issues
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using them
        pool_size=5,  # Maintain 5 connections in the pool
        max_overflow=10,  # Allow up to 10 additional connections
        pool_recycle=3600,  # Recycle connections after 1 hour
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        # Rollback on exception
        db.rollback()
        raise
    finally:
        db.close()

from . import models  # noqa: E402

def init_db():
    Base.metadata.create_all(bind=engine)
