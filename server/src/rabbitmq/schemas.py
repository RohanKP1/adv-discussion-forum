from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificationMessage(BaseModel):
    """
    Pydantic model for notification messages that matches both 
    the database model and messaging requirements.
    """
    user_id: int
    message: str
    content: Optional[str] = None
    notification_type: Optional[str] = None
    reference_id: Optional[int] = None
    notification_id: Optional[int] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_read: Optional[bool] = False

    class Config:
        from_attributes = True
        # Allows conversion from ORM models