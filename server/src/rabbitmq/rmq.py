import time
import pika
import logging
from contextlib import contextmanager
from server.src.core.config import settings
from server.src.rabbitmq.schemas import NotificationMessage

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RabbitMQConnection:
    _connection = None
    _channel = None

    @classmethod
    @contextmanager
    def get_connection(cls):
        try:
            if not cls._connection or cls._connection.is_closed:
                cls._connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
                cls._channel = cls._connection.channel()
                
                # Declare exchanges and queues
                cls._channel.exchange_declare(exchange='notifications', exchange_type='topic')
                cls._channel.queue_declare(queue='user_notifications')
                cls._channel.queue_bind(exchange='notifications', queue='user_notifications', routing_key='user.*')
            
            yield cls._channel
        except (pika.exceptions.AMQPError, ConnectionError) as e:
            logger.error(f"RabbitMQ connection error: {e}")
            if cls._connection:
                cls._connection.close()
            raise
        finally:
            if cls._connection and not cls._connection.is_closed:
                cls._connection.close()

def publish_message(routing_key: str, message: NotificationMessage):
    """
    Publish a message to a RabbitMQ exchange with improved error handling.
    """
    try:
        with RabbitMQConnection.get_connection() as channel:
            channel.basic_publish(
                exchange='notifications',
                routing_key=routing_key,
                body=message.model_dump_json(),
                properties=pika.BasicProperties(content_type='application/json')
            )
            logger.info(f"Message published with routing key: {routing_key}")
    except Exception as e:
        logger.error(f"Failed to publish message: {e}")
        raise

def consume_messages(queue: str, callback, max_retries=3):
    """
    Consume messages from a RabbitMQ queue with retry mechanism.
    """
    retries = 0
    while retries < max_retries:
        try:
            with RabbitMQConnection.get_connection() as channel:
                def on_message(ch, method, properties, body):
                    try:
                        message = NotificationMessage.parse_raw(body)
                        callback(message)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")

                channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)
                logger.info(f"Started consuming messages from queue: {queue}")
                channel.start_consuming()
        except Exception as e:
            logger.error(f"Error in message consumption (Retry {retries + 1}/{max_retries}): {e}")
            retries += 1
            time.sleep(2 ** retries)  # Exponential backoff

def handle_notification(message: NotificationMessage):
    """
    Handle the received notification with improved logging.
    """
    logger.debug(f"Received notification: {message}")
    # Add your notification handling logic here