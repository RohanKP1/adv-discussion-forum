from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from server.src.db.session import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    topics = relationship(
        "Topic", back_populates="user", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    subscriptions = relationship(
        "UserTopicSubscription", back_populates="user", cascade="all, delete-orphan"
    )

class Topic(Base):
    __tablename__ = 'topics'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    view_count = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False)
    
    user = relationship(__module__ + ".User", back_populates="topics")
    comments = relationship(__module__ + ".Comment", back_populates="topic")
    tags = relationship(__module__ + ".Tag", secondary="topic_tags", back_populates="topics")
    subscriptions = relationship(__module__ + ".UserTopicSubscription", back_populates="topic")

    def __lt__(self, other):
        return self.trending_score < other.trending_score

class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    
    topic = relationship(__module__ + ".Topic", back_populates="comments")
    user = relationship(__module__ + ".User", back_populates="comments")
    replies = relationship(__module__ + ".Comment", back_populates="parent", remote_side=[id])
    parent = relationship(__module__ + ".Comment", back_populates="replies", remote_side=[parent_id])

class Notification(Base):
    __tablename__ = 'notifications'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    notification_type = Column(String, nullable=False)
    reference_id = Column(Integer, nullable=True)
    
    user = relationship(__module__ + ".User", back_populates="notifications")

class UserTopicSubscription(Base):
    __tablename__ = 'user_topic_subscriptions'
    __table_args__ = {'extend_existing': True}
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    subscribed_at = Column(DateTime, default=datetime.now)
    notification_preference = Column(String, default="all")
    
    user = relationship(__module__ + ".User", back_populates="subscriptions")
    topic = relationship(__module__ + ".Topic", back_populates="subscriptions")

class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    topics = relationship(__module__ + ".Topic", secondary="topic_tags", back_populates="tags")

topic_tags = Table(
    'topic_tags', Base.metadata,
    Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    extend_existing=True
)

