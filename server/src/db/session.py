from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server.src.core.config import settings

# Create these variables but don't initialize the engine yet
database_url = settings.DATABASE_URL
engine = None
SessionLocal = None
Base = declarative_base()

def setup_db():
    global engine, SessionLocal
    # Only initialize if not already done
    if engine is None:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)

def get_db():
    # Ensure the database is set up
    if SessionLocal is None:
        setup_db()
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()