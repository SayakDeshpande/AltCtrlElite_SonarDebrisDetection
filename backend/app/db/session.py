"""SQLAlchemy engine and session factory.

Importing this module configures SQLAlchemy only; it does not open a database
connection. A connection is made only when a session is used.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Yield a database session for future application dependencies."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
