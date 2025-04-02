import logging
from sqlalchemy.orm import Session
from server.src.db.session import get_db
from server.src.rabbitmq.rmq import publish_message, consume_messages
from server.src.rabbitmq.schemas import NotificationMessage
from server.src.db.models import Notification, User

def create_notification(db: Session, user_id: int, content: str, notification_type: str, reference_id: int):
    """
    Create a notification in the database and publish it to RabbitMQ
    """
    try:
        # Create notification in the database
        notification = Notification(
            user_id=user_id,
            content=content,
            notification_type=notification_type,
            reference_id=reference_id,
            is_read=False
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)

        # Publish message to RabbitMQ
        message = NotificationMessage(
            user_id=user_id,
            message=content,
            content=content,
            notification_type=notification_type,
            reference_id=reference_id,
            notification_id=notification.id,
            timestamp=notification.created_at,
            is_read=False
        )
        
        publish_message(f"user.{user_id}", message)
        
        logging.info(f"Notification created and published for user {user_id}")
        return notification
    
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating notification: {e}")
        raise

def remove_notification(db: Session, notification_id: int):
    """
    Remove a notification from the database
    """
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if notification:
            db.delete(notification)
            db.commit()
            logging.info(f"Notification {notification_id} removed successfully")
        else:
            logging.warning(f"Notification {notification_id} not found")
    
    except Exception as e:
        db.rollback()
        logging.error(f"Error removing notification: {e}")
        raise

def notification_consumer(message: NotificationMessage):
    """
    Consume notifications from RabbitMQ and process them
    """
    try:
        db = next(get_db())
        
        # Process the notification (you can add custom logic here)
        logging.info(f"Processing notification: {message}")
        
        # Optional: Mark notification as read or perform other actions
        if message.notification_id:
            notification = db.query(Notification).filter(Notification.id == message.notification_id).first()
            if notification:
                notification.is_read = True
                db.commit()
        
    except Exception as e:
        logging.error(f"Error in notification consumer: {e}")
    finally:
        db.close()

def start_notification_service():
    """
    Start the notification service to consume messages
    """
    logging.basicConfig(level=logging.INFO)
    consume_messages('user_notifications', notification_consumer)

# Example usage
def example_notification_workflow():
    db = next(get_db())
    try:
        # Assume we have a user with ID 1
        user_id = 1
        
        # Create a new notification
        new_notification = create_notification(
            db, 
            user_id=user_id, 
            content="New comment on your topic", 
            notification_type="comment", 
            reference_id=4  # ID of the related comment or topic
        )
        
        # Remove the notification
        # remove_notification(db, new_notification.id)
    
    except Exception as e:
        logging.error(f"Error in notification workflow: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Uncomment to start consuming notifications
    # start_notification_service()
    
    # Example workflow demonstration
    example_notification_workflow()