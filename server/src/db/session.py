from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from src.core.config import settings
# from src.rabbitmq.rmq import publish_message
# from src.rabbitmq.schemas import NotificationMessage

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
        # Notify RabbitMQ when a session is created
        # message = NotificationMessage(user_id=0, message="New DB session created")
        # publish_message("db.session.created", message)
        yield db
    finally:
        db.close()
        # Notify RabbitMQ when a session is closed
        # message = NotificationMessage(user_id=0, message="DB session closed")
        # publish_message("db.session.closed", message)