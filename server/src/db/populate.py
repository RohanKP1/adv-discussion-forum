from sqlalchemy.orm import Session
from server.src.db.session import get_db
from server.src.db.models import User, Topic, Comment, Notification, UserTopicSubscription, Tag
from server.src.utils.security import hash_password
from datetime import datetime, timezone

def add_example_data(db: Session):
    # Create example users
    user1 = User(
        username="user1",
        email="user1@example.com",
        password_hash=hash_password("password1"),
        created_at=datetime.now(timezone.now),
        bio="Bio of user1",
        avatar_url="http://example.com/avatar1.png"
    )
    user2 = User(
        username="user2",
        email="user2@example.com",
        password_hash=hash_password("password2"),
        created_at=datetime.now(timezone.now),
        bio="Bio of user2",
        avatar_url="http://example.com/avatar2.png"
    )
    db.add(user1)
    db.add(user2)
    db.commit()

    # Create example topics
    topic1 = Topic(
        title="Topic 1",
        content="Content of topic 1",
        user_id=user1.id,
        created_at=datetime.now(timezone.now),
        view_count=10,
        is_locked=False
    )
    topic2 = Topic(
        title="Topic 2",
        content="Content of topic 2",
        user_id=user2.id,
        created_at=datetime.now(timezone.now),
        view_count=20,
        is_locked=False
    )
    db.add(topic1)
    db.add(topic2)
    db.commit()

    # Create example comments
    comment1 = Comment(
        content="Comment 1 on topic 1",
        topic_id=topic1.id,
        user_id=user2.id,
        created_at=datetime.now(timezone.now)
    )
    comment2 = Comment(
        content="Comment 2 on topic 2",
        topic_id=topic2.id,
        user_id=user1.id,
        created_at=datetime.now(timezone.now)
    )
    db.add(comment1)
    db.add(comment2)
    db.commit()

    # Create example notifications
    notification1 = Notification(
        user_id=user1.id,
        content="Notification 1 for user1",
        is_read=False,
        created_at=datetime.now(timezone.now),
        notification_type="comment",
        reference_id=comment1.id
    )
    notification2 = Notification(
        user_id=user2.id,
        content="Notification 2 for user2",
        is_read=False,
        created_at=datetime.now(timezone.now),
        notification_type="comment",
        reference_id=comment2.id
    )
    db.add(notification1)
    db.add(notification2)
    db.commit()

    # Create example user-topic subscriptions
    subscription1 = UserTopicSubscription(
        user_id=user1.id,
        topic_id=topic2.id,
        subscribed_at=datetime.now(timezone.now),
        notification_preference="all"
    )
    subscription2 = UserTopicSubscription(
        user_id=user2.id,
        topic_id=topic1.id,
        subscribed_at=datetime.now(timezone.now),
        notification_preference="mentions"
    )
    db.add(subscription1)
    db.add(subscription2)
    db.commit()

    # Create example tags
    tag1 = Tag(
        name="Tag1",
        description="Description of tag1"
    )
    tag2 = Tag(
        name="Tag2",
        description="Description of tag2"
    )
    db.add(tag1)
    db.add(tag2)
    db.commit()

    # Associate tags with topics
    topic1.tags.append(tag1)
    topic2.tags.append(tag2)
    db.commit()

def populate_main():
    db = next(get_db())
    add_example_data(db)
    db.close()