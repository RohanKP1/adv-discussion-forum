import strawberry

@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: str
    last_login: str
    bio: str
    avatar_url: str

@strawberry.type
class TopicType:
    id: int
    title: str
    content: str
    user_id: int
    created_at: str
    updated_at: str = None
    view_count: int = 0
    is_locked: bool

@strawberry.type
class CommentType:
    id: int
    topic_id: int
    content: str
    user_id: int
    created_at: str
    updated_at: str
    parent_id: int

@strawberry.type
class NotificationType:
    id: int
    user_id: int
    content: str
    is_read: bool
    created_at: str
    notification_type: str
    reference_id: int

@strawberry.type
class UserTopicSubscriptionType:
    id: int
    user_id: int
    topic_id: int
    subscribed_at: str
    notification_preference: str

@strawberry.type
class TagType:
    id: int
    title: str
    content: str
    user_id: int
    created_at: str
    is_locked: bool



    