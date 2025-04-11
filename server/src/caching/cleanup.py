from server.src.caching.connector import get_redis_connection

def clear_user_cache(user_id: int):
    """
    Clear all Redis cache related to a specific user.
    """
    try:
        redis_client = get_redis_connection()
        keys = redis_client.keys(f"user:{user_id}:*")
        for key in keys:
            redis_client.delete(key)
        print(f"Cleared Redis cache for user {user_id}")
    except Exception as e:
        print(f"Error clearing Redis cache for user {user_id}: {e}")
        raise