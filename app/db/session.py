from typing import Generator
from sqlalchemy.orm import Session
from app.db.base import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields database sessions.
    Used by FastAPI dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseSession:
    """
    Context manager for database sessions.
    Usage:
        with DatabaseSession() as db:
            # do something with db
    """
    def __init__(self):
        self.db = None

    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            if exc_type is not None:
                # If an exception occurred, rollback the session
                self.db.rollback()
            else:
                # If no exception occurred, commit the session
                self.db.commit()
            self.db.close()

def get_db_session() -> DatabaseSession:
    """
    Factory function that returns a new DatabaseSession instance.
    Usage:
        db_session = get_db_session()
        with db_session as db:
            # do something with db
    """
    return DatabaseSession() 