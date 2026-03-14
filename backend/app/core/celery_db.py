from core.database import engine
from core.config import get_settings

settings = get_settings()

class DatabaseConnection:
    """Database connection for Celery tasks"""
    
    @staticmethod
    def get_session():
        """Get database session for Celery"""
        from sqlalchemy.orm import sessionmaker
        from core.database import Base
        
        engine.connect()
        Base.metadata.create_all(bind=engine)
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
