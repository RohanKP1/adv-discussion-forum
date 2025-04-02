from datetime import datetime, timedelta
import heapq
import json
from sqlalchemy import func
import strawberry
from strawberry.asgi import GraphQL
from fastapi import HTTPException
from server.src.graphql.schema import TopicType, UserType, CommentType, TagType, NotificationType
from server.src.db.models import Topic, Comment, User, Notification
from server.src.db.session import get_db
from server.src.api.login import get_current_user  
from server.src.utils.tries import Trie
from server.src.rabbitmq.notification import create_notification
from server.src.redis.connector import get_redis_connection

topic_trie = Trie()

def load_topics_into_trie():
    """
    Load topics from the database into the Trie.
    """
    db = next(get_db())
    topics = db.query(Topic).all()
    for topic in topics:
        topic_trie.insert(
            topic.title,
            {
                "id": topic.id,
                "title": topic.title,
                "content": topic.content,
                "user_id": topic.user_id,
                "created_at": topic.created_at.isoformat(),
                "is_locked": topic.is_locked  # Include is_locked
            },
        )
    db.close()

def search_topics(query):
    """
    Search for topics in the Trie.
    """
    load_topics_into_trie()
    return topic_trie.search(query)

def get_user_from_context(info) -> UserType:
    """Extract user from FastAPI request context."""
    request = info.context["request"]
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = token.split("Bearer ")[1]
    with next(get_db()) as db:
        user = get_current_user(db, token)
        return user
    
def _compute_trending_topics(user, time_window, max_topics):
    """
    Core logic for computing trending topics.
    Extracted to a separate function to improve readability and reusability.
    """
    db = next(get_db())
    
    try:
        # Calculate the date threshold for the time window
        time_threshold = datetime.utcnow() - timedelta(days=time_window)
        
        # Subquery to get comment counts for each topic within the time window
        recent_comment_counts = (
            db.query(Comment.topic_id, func.count(Comment.id).label('recent_comment_count'))
            .filter(Comment.created_at >= time_threshold)
            .group_by(Comment.topic_id)
            .subquery()
        )
            
        # Subquery to get total comment counts for each topic
        total_comment_counts = (
            db.query(Comment.topic_id, func.count(Comment.id).label('total_comment_count'))
            .group_by(Comment.topic_id)
            .subquery()
        )
            
        # Main query to get topics with comment metrics
        trending_query = (
            db.query(
                Topic, 
                recent_comment_counts.c.recent_comment_count,
                total_comment_counts.c.total_comment_count
            )
            .outerjoin(recent_comment_counts, Topic.id == recent_comment_counts.c.topic_id)
            .outerjoin(total_comment_counts, Topic.id == total_comment_counts.c.topic_id)
            .all()
        )
            
        # Create a min-heap to store top trending topics
        trending_heap = []
        
        for topic, recent_comments, total_comments in trending_query:
            # Scoring logic
            recent_comment_weight = recent_comments or 0
            total_comment_weight = total_comments or 0
            recency_weight = max(0, 1 - (datetime.utcnow() - topic.created_at).days / time_window)
            
            # Trending score calculation
            trending_score = (
                recent_comment_weight * 2 +  # Higher weight for recent comments
                total_comment_weight * 1 +   # Lower weight for total comments
                recency_weight * 3           # Higher weight for recent topics
            )
            
            # Use heapq to maintain top trending topics
            if len(trending_heap) < max_topics:
                heapq.heappush(trending_heap, (trending_score, topic.id, topic))
            else:
                # If heap is full, push and pop to keep only top max_topics
                heapq.heappushpop(trending_heap, (trending_score, topic.id, topic))
        
        # Sort the heap in descending order of trending score
        trending_topics = sorted(trending_heap, reverse=True)
        
        # Extract and return topics
        return [topic for _, _, topic in trending_topics]
    
    finally:
        db.close()    

@strawberry.type
class Query:
    @strawberry.field
    def hello(self, info, user_id: int) -> str:
        with next(get_db()) as db:
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        
        return user.username
        
        # Create a notification instead of publishing a RabbitMQ message
        # with next(get_db()) as db:
        #     create_notification(
        #         db, 
        #         user_id=user.id, 
        #         content=f"Hello User: {user.username}!", 
        #         notification_type="greeting",
        #         reference_id=user.id
        #     )
        
        # return f"Hello, {user.username}!"

    @strawberry.field
    def get_all_topics(self, info) -> list[TopicType]:
        user = get_user_from_context(info)
        db = next(get_db())
        try:
            topics = db.query(Topic).all()
            return topics
        finally:
            db.close()

    @strawberry.field
    def get_topic_by_name(self, title: str, info) -> TopicType:
        user = get_user_from_context(info)
        db = next(get_db())
        try:
            topic = db.query(Topic).filter_by(title=title).first()
            return topic
        finally:
            db.close()

    @strawberry.field
    def search_topics(self, prefix: str, info) -> list[TagType]:
        """
        Search for topics using a Trie.
        """
        results = search_topics(prefix)
        return [
            TagType(
                id=t["id"],
                title=t["title"],
                content=t["content"],
                user_id=t["user_id"],
                created_at=t["created_at"],
                is_locked=t["is_locked"]
            )
            for t in results
        ]    

    
    @strawberry.field
    def get_topics_by_user(self, info) -> list[TopicType]:
        user = get_user_from_context(info)
        db = next(get_db())
        try:
            topics = db.query(Topic).filter_by(user_id=user.id).all()
            return topics
        finally:
            db.close()

    @strawberry.field
    def get_comments_by_topic_id(self, topic_id: int, info) -> list[CommentType]:
        user = get_user_from_context(info)
        db = next(get_db())
        try:
            comments = db.query(Comment).filter_by(topic_id=topic_id).all()
            return comments
        finally:
            db.close()
        
    @strawberry.field
    def get_trending_topics(self, 
                            info, 
                            time_window: int = 7, 
                            max_topics: int = 10) -> list[TopicType]:
        """
        Retrieve trending topics with Redis caching.
        
        Args:
            time_window (int): Number of days to consider for trending topics. Default is 7 days.
            max_topics (int): Maximum number of trending topics to return. Default is 10.
        """
        user = get_user_from_context(info)
        
        # Try to get Redis connection
        try:
            redis_client = get_redis_connection()
        except Exception:
            # Fallback to computing without caching if Redis is unavailable
            # Log this in a production environment
            return _compute_trending_topics(user, time_window, max_topics)
        
        # Create a unique cache key based on parameters
        cache_key = f"trending_topics:{time_window}:{max_topics}"
        
        try:
            # Try to fetch from Redis cache first
            cached_trending_topics = redis_client.get(cache_key)
            if cached_trending_topics:
                # Deserialize cached topics
                cached_topics = json.loads(cached_trending_topics)
                return [TopicType(**topic) for topic in cached_topics]
            
            # If not in cache, compute trending topics
            result_topics = _compute_trending_topics(user, time_window, max_topics)
            
            # Serialize topics for caching (convert to dict)
            serializable_topics = [
                {
                    "id": topic.id, 
                    "title": topic.title, 
                    "content": topic.content,
                    "user_id": topic.user_id,
                    "created_at": topic.created_at.isoformat(),
                    "is_locked": topic.is_locked
                } for topic in result_topics
            ]
            
            # Cache the results in Redis with an expiration (e.g., 1 hour)
            redis_client.setex(
                cache_key, 
                3600,  # 1 hour cache expiration 
                json.dumps(serializable_topics)
            )
            
            return result_topics
        
        finally:
            # Ensure Redis connection is closed
            if redis_client:
                redis_client.close()

    
    @strawberry.field
    def get_user_notifications(self, info) -> list[NotificationType]:
        """
        Retrieve unread notifications for the current user.
        """
        user = get_user_from_context(info)
        with next(get_db()) as db:
            notifications = (
                db.query(Notification)  # Note: querying Notification model directly
                .filter_by(user_id=user.id)  # Use 'read' here
                .order_by(Notification.created_at.desc())
                .all()
            )
            return notifications

@strawberry.type
class Mutation:
    @strawberry.field
    def create_topic(self, title: str, content: str, is_locked: bool, info) -> TopicType:
        user = get_user_from_context(info)
        with next(get_db()) as db:
            existing_topic = db.query(Topic).filter_by(title=title, user_id=user.id).first()
            if existing_topic:
                raise ValueError("Topic with the given title already exists for this user.")
            
            topic = Topic(title=title, content=content, user_id=user.id, is_locked=is_locked)
            db.add(topic)

            # Create a notification about the new topic
            create_notification(
                db, 
                user_id=user.id, 
                content=f"New topic created: {title}", 
                notification_type="topic_created",
                reference_id=topic.id  # Use the topic's ID after it is committed
            )

            db.commit()  # Commit the session to persist the topic
            db.refresh(topic)  # Refresh the topic to bind it to the session

            return topic

    @strawberry.field
    def delete_topic(self, topic_id: int, info) -> bool:
        user = get_user_from_context(info)
        try:
            with next(get_db()) as db:
                topic = db.query(Topic).filter_by(id=topic_id, user_id=user.id).first()
                if not topic:
                    raise HTTPException(status_code=404, detail="Topic not found or unauthorized")
                
                # Optional: Delete associated comments first
                db.query(Comment).filter_by(topic_id=topic_id).delete()
                
                # Create a notification about topic deletion
                create_notification(
                    db, 
                    user_id=user.id, 
                    content=f"Topic deleted: {topic.title}", 
                    notification_type="topic_deleted",
                    reference_id=user.id
                )
                
                db.delete(topic)
                db.commit()
                
                return True
        except Exception as e:
            # Log the error
            print(f"Error deleting topic: {e}")
            # Rollback the transaction
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete topic")

    @strawberry.field    
    def update_topic(self, topic_id: int, title: str, content: str, info) -> TopicType:
        user = get_user_from_context(info)
        with next(get_db()) as db:
            topic = db.query(Topic).filter_by(id=topic_id, user_id=user.id).first()
            if topic:
                topic.title = title
                topic.content = content
                db.commit()  # Commit the changes to persist them in the database
                db.refresh(topic)  # Refresh the topic to reflect the updated state
                return topic
            raise HTTPException(status_code=404, detail="Topic not found or unauthorized")
        
    @strawberry.field
    def create_comment(self, topic_id: int, content: str, info) -> CommentType:
        user = get_user_from_context(info)
        with next(get_db()) as db:  
            comment = Comment(topic_id=topic_id, content=content, user_id=user.id)
            db.add(comment)

            # Create a notification about the new comment
            # Get the topic to include its title in the notification
            topic = db.query(Topic).filter_by(id=topic_id).first()
            if topic:
                # Notify the topic creator
                create_notification(
                    db, 
                    user_id=topic.user_id,  # Notify the topic creator
                    content=f"New comment on your topic: {topic.title}", 
                    notification_type="comment_created",
                    reference_id=comment.id
                )

            db.commit()
            db.refresh(comment)
            
            return comment


        user = get_user_from_context(info)
        with next(get_db()) as db:  
            comment = Comment(topic_id=topic_id, content=content, user_id=user.id)
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment

    @strawberry.field
    def delete_comment(self, comment_id: int, info) -> bool:
        user = get_user_from_context(info)
        with next(get_db()) as db:
            comment = db.query(Comment).filter_by(id=comment_id, user_id=user.id).first()
            if comment:
                db.delete(comment)
                return True
            return False

    @strawberry.field
    def update_comment(self, comment_id: int, content: str, info) -> CommentType:
        user = get_user_from_context(info)
        with next(get_db()) as db:
            comment = db.query(Comment).filter_by(id=comment_id, user_id=user.id).first()
            if comment:
                comment.content = content
                db.commit()  # Commit the changes to persist them in the database
                db.refresh(comment)  # Refresh the comment to reflect the updated state
                return comment
            return None
        
    @strawberry.field
    def mark_notification_read(self, notification_id: int, info) -> bool:
        """
        Mark a specific notification as read.
        """
        user = get_user_from_context(info)
        with next(get_db()) as db:
            notification = (
                db.query(Notification)
                .filter_by(id=notification_id, user_id=user.id)
                .first()
            )
            
            if not notification:
                return False
            
            notification.is_read = True
            db.commit()
            return True

    @strawberry.field
    def mark_all_notifications_read(self, info) -> bool:
        """
        Mark all notifications for the current user as read.
        """
        user = get_user_from_context(info)
        with next(get_db()) as db:
            db.query(Notification).filter_by(user_id=user.id, is_read=False).update({
                'is_read': True
            })
            db.commit()
            return True    

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = GraphQL(schema)
