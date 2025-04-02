import requests
from typing import Dict, Any, Optional
from .auth import AuthClient

class GraphQLClient:
    def __init__(self, base_url: str = "http://localhost:8000/graphql", auth_client: Optional[AuthClient] = None):
        """
        Initialize GraphQL Client
        
        Args:
            base_url (str): GraphQL endpoint URL
            auth_client (AuthClient, optional): Authentication client for headers
        """
        self.base_url = base_url
        self.auth_client = auth_client

    def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a GraphQL query
        
        Args:
            query (str): GraphQL query string
            variables (dict, optional): Variables for the query
        
        Returns:
            Dict or None: Query result or None if error
        """
        headers = {
            "Content-Type": "application/json",
            **(self.auth_client.get_headers() if self.auth_client else {})
        }
        
        payload = {
            "query": query,
            "variables": variables or {}
        }

        try:
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GraphQL Query Error: {e}")
            return None

    def hello(self, user_id: int) -> Optional[str]:
        query = """
        query {
            hello(userId: %d)
        }
        """ % user_id
        
        result = self.execute_query(query)
        return result['data']['hello'] if result and 'data' in result else None

    def get_all_topics(self) -> Optional[list]:
        """
        Fetch all topics
        
        Returns:
            list or None: List of topics or None if error
        """
        query = """
        query {
            getAllTopics {
                id
                title
                content
                createdAt
                isLocked
                userId
            }
        }
        """
        result = self.execute_query(query)
        if result['data'] is None:
            return None
        return result['data']['getAllTopics']

    def get_topic_by_name(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a topic by its title
        
        Args:
            title (str): Topic title
        
        Returns:
            Dict or None: Topic details or None if error
        """
        query = """
        query GetTopicByName($title: String!) {
            getTopicByName(title: $title) {
                id
                title
                content
                createdAt
                isLocked
                userId
            }
        }
        """
        variables = {"title": title}
        result = self.execute_query(query, variables)
        return result['data']['getTopicByName'] if result and 'data' in result else None

    def get_topics_by_user(self) -> Optional[list]:
        """
        Fetch topics created by the current user
        
        Returns:
            list or None: List of user's topics or None if error
        """
        query = """
        query {
            getTopicsByUser {
                id
                title
                content
                createdAt
                isLocked
            }
        }
        """
        result = self.execute_query(query)
        return result['data']['getTopicsByUser'] if result and 'data' in result else None

    def search_topics(self, prefix: str) -> Optional[list]:
        """
        Search topics by prefix
        
        Args:
            prefix (str): Search prefix
        
        Returns:
            list or None: Matching topics or None if error
        """
        query = """
        query SearchTopics($prefix: String!) {
            searchTopics(prefix: $prefix) {
                id
                title
                content
                userId
                createdAt
                isLocked
            }
        }
        """
        variables = {"prefix": prefix}
        result = self.execute_query(query, variables)
        return result['data']['searchTopics'] if result and 'data' in result else None

    def get_comments_by_topic_id(self, topic_id: int) -> Optional[list]:
        """
        Fetch comments for a specific topic
        
        Args:
            topic_id (int): ID of the topic
        
        Returns:
            list or None: List of comments or None if error
        """
        query = """
        query GetCommentsByTopicId($topic_id: Int!) {
            getCommentsByTopicId(topicId: $topic_id) {
                id
                content
                createdAt
                userId
                topicId
            }
        }
        """
        variables = {"topic_id": topic_id}
        result = self.execute_query(query, variables)
        return result['data']['getCommentsByTopicId'] if result and 'data' in result else None

    def get_trending_topics(self, time_window: int = 7, max_topics: int = 3) -> Optional[list]:
        """
        Fetch trending topics
        
        Args:
            time_window (int, optional): Number of days to consider. Defaults to 7.
            max_topics (int, optional): Maximum number of topics to return. Defaults to 10.
        
        Returns:
            list or None: List of trending topics or None if error
        """
        query = """
        query GetTrendingTopics($time_window: Int, $max_topics: Int) {
            getTrendingTopics(timeWindow: $time_window, maxTopics: $max_topics) {
                id
                title
                content
                createdAt
                isLocked
                userId
            }
        }
        """
        variables = {
            "time_window": time_window,
            "max_topics": max_topics
        }
        result = self.execute_query(query, variables)
        return result['data']['getTrendingTopics'] if result and 'data' in result else None

    def get_user_notifications(self) -> Optional[list]:
        """
        Fetch user notifications
        
        Returns:
            list or None: List of user notifications or None if error
        """
        query = """
        query {
            getUserNotifications {
                id
                content
                createdAt
                userId
                isRead
            }
        }
        """
        result = self.execute_query(query)
        return result['data']['getUserNotifications'] if result and 'data' in result else None

    def create_topic(self, title: str, content: str, is_locked: bool = False) -> Optional[Dict[str, Any]]:
        """
        Create a new topic
        
        Args:
            title (str): Topic title
            content (str): Topic content
            is_locked (bool, optional): Whether topic is locked
        
        Returns:
            Dict or None: Created topic details or None if error
        """
        mutation = """
        mutation CreateTopic($title: String!, $content: String!, $is_locked: Boolean!) {
            createTopic(title: $title, content: $content, isLocked: $is_locked) {
                id
                title
                content
                createdAt
                isLocked
                userId
            }
        }
        """
        variables = {
            "title": title,
            "content": content,
            "is_locked": is_locked
        }
        
        result = self.execute_query(mutation, variables)
        return result['data']['createTopic'] if result and 'data' in result else None

    def delete_topic(self, topic_id: int) -> Optional[bool]:
        """
        Delete a topic
        
        Args:
            topic_id (int): ID of the topic to delete
        
        Returns:
            bool or None: True if deleted, None if error
        """
        mutation = """
        mutation DeleteTopic($topic_id: Int!) {
            deleteTopic(topicId: $topic_id)
        }
        """
        variables = {"topic_id": topic_id}
        
        result = self.execute_query(mutation, variables)
        return result['data']['deleteTopic'] if result and 'data' in result else None

    def update_topic(self, topic_id: int, title: str, content: str) -> Optional[Dict[str, Any]]:
        """
        Update an existing topic
        
        Args:
            topic_id (int): ID of the topic to update
            title (str): New topic title
            content (str): New topic content
        
        Returns:
            Dict or None: Updated topic details or None if error
        """
        mutation = """
        mutation UpdateTopic($topic_id: Int!, $title: String!, $content: String!) {
            updateTopic(topicId: $topic_id, title: $title, content: $content) {
                id
                title
                content
                createdAt
                isLocked
                userId
            }
        }
        """
        variables = {
            "topic_id": topic_id,
            "title": title,
            "content": content
        }
        
        result = self.execute_query(mutation, variables)
        return result['data']['updateTopic'] if result and 'data' in result else None

    def create_comment(self, topic_id: int, content: str) -> Optional[Dict[str, Any]]:
        """
        Create a new comment on a topic
        
        Args:
            topic_id (int): ID of the topic to comment on
            content (str): Comment content
        
        Returns:
            Dict or None: Created comment details or None if error
        """
        mutation = """
        mutation CreateComment($topic_id: Int!, $content: String!) {
            createComment(topicId: $topic_id, content: $content) {
                id
                content
                createdAt
                userId
                topicId
            }
        }
        """
        variables = {
            "topic_id": topic_id,
            "content": content
        }
        
        result = self.execute_query(mutation, variables)
        return result['data']['createComment'] if result and 'data' in result else None

    def delete_comment(self, comment_id: int) -> Optional[bool]:
        """
        Delete a comment
        
        Args:
            comment_id (int): ID of the comment to delete
        
        Returns:
            bool or None: True if deleted, None if error
        """
        mutation = """
        mutation DeleteComment($comment_id: Int!) {
            deleteComment(commentId: $comment_id)
        }
        """
        variables = {"comment_id": comment_id}
        
        result = self.execute_query(mutation, variables)
        return result['data']['deleteComment'] if result and 'data' in result else None

    def update_comment(self, comment_id: int, content: str) -> Optional[Dict[str, Any]]:
        """
        Update an existing comment
        
        Args:
            comment_id (int): ID of the comment to update
            content (str): New comment content
        
        Returns:
            Dict or None: Updated comment details or None if error
        """
        mutation = """
        mutation UpdateComment($comment_id: Int!, $content: String!) {
            updateComment(commentId: $comment_id, content: $content) {
                id
                content
                createdAt
                userId
                topicId
            }
        }
        """
        variables = {
            "comment_id": comment_id,
            "content": content
        }
        
        result = self.execute_query(mutation, variables)
        return result['data']['updateComment'] if result and 'data' in result else None

    def mark_notification_read(self, notification_id: int) -> Optional[bool]:
        """
        Mark a specific notification as read
        
        Args:
            notification_id (int): ID of the notification to mark as read
        
        Returns:
            bool or None: True if marked, None if error
        """
        mutation = """
        mutation MarkNotificationRead($notification_id: Int!) {
            markNotificationRead(notificationId: $notification_id)
        }
        """
        variables = {"notification_id": notification_id}
        
        result = self.execute_query(mutation, variables)
        return result['data']['markNotificationRead'] if result and 'data' in result else None

    def mark_all_notifications_read(self) -> Optional[bool]:
        """
        Mark all notifications as read
        
        Returns:
            bool or None: True if marked, None if error
        """
        mutation = """
        mutation MarkAllNotificationsRead {
            markAllNotificationsRead
        }
        """
        
        result = self.execute_query(mutation)
        return result['data']['markAllNotificationsRead'] if result and 'data' in result else None