import redis
from server.src.core.config import settings

def get_redis_connection():
    """
    Establish a Redis connection using the URL from settings.
    
    Returns:
        redis.Redis: A Redis client connection
    """
    try:
        # Use from_url to create Redis connection from the REDIS_URL
        return redis.from_url(settings.REDIS_URL)
    except Exception as e:
        # Add proper logging in a production environment
        print(f"Redis connection error: {e}")
        raise