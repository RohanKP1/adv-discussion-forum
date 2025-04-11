# Adv Real-Time Discussion Forum

This project is an implementation of a web application using FastAPI and GraphQL, with support for user authentication, notifications via RabbitMQ, and data storage using SQLAlchemy.

## Features

- User Registration and Authentication
- Topic and Comment Management
- Notification System using RabbitMQ
- GraphQL API with Mutations and Queries
- Database Integration with SQLAlchemy

## Folder Structure

```
adv-discussion-forum/
├── client/
│   ├── app.py                          # Entry point for the Streamlit application
│   ╰── src/
│       ├── __init__.py                 # Initialization file for the client package
│       ├── components/                 # Streamlit UI components
│       │   ├── dashboard.py            # Main dashboard page
│       │   ├── login.py                # Login page
│       │   ├── register.py             # Registration page
│       │   ╰── pages/                  # Subpages for the dashboard
│       │       ├── home_page.py        # Home page with trending topics
│       │       ├── create_topic.py     # Page to create a new topic
│       │       ├── content_hub.py      # User's topics and comments management
│       │       ├── notifications.py    # Notifications page
│       │       ├── search_topics.py    # Search topics page
│       │       ├── user_profile.py     # User profile page
│       │       ╰── display_comments.py # Helper for displaying comments
│       ╰── services/                   # Backend service clients
│           ├── auth.py                 # Authentication client
│           ├── graphql_client.py       # GraphQL client
│           ╰── api_client.py           # REST API client
├── server/
│   ├── main.py                         # Entry point for the FastAPI server
│   ├── src/
│   │   ├── api/                        # FastAPI endpoints
│   │   │   ├── login.py                # User authentication and management
│   │   │   ╰── schemas.py              # Pydantic models for API
│   │   ├── core/                       # Core configuration
│   │   │   ╰── config.py               # Application settings
│   │   ├── db/                         # Database models and utilities
│   │   │   ├── models.py               # SQLAlchemy models
│   │   │   ├── session.py              # Database session setup
│   │   │   ├── crud.py                 # CRUD operations
│   │   │   ├── populate.py             # Populate database with example data
│   │   │   ╰── test.py                 # Test database setup
│   │   ├── graphql/                    # GraphQL API
│   │   │   ├── gql.py                  # GraphQL queries and mutations
│   │   │   ╰── schema.py               # GraphQL schema definitions
│   │   ├── rabbitmq/                   # RabbitMQ integration
│   │   │   ├── rmq.py                  # RabbitMQ connection and utilities
│   │   │   ├── notification.py         # Notification handling
│   │   │   ╰── schemas.py              # Pydantic models for RabbitMQ messages
│   │   ├── caching/                      # Redis integration
│   │   │   ├── connector.py            # Redis connection setup
│   │   │   ╰── cleanup.py              # Redis cleanup utilities
│   │   ╰── utils/                      # Utility functions
│   │       ├── security.py             # Password hashing and JWT utilities
│   │       ╰── tries.py                # Trie data structure for search
│   ╰── tests/                          # Test cases for the server
│       ├── test_login.py               # Tests for login endpoints
│       ╰── api_service.py              # Mock API service for testing
├── .streamlit/
│   ╰── config.toml                     # Streamlit configuration
├── docker-compose.yml                  # Docker Compose configuration
├── requirements.txt                    # Python dependencies
├── readme.md                           # Project documentation
├── LICENSE                             # License file
╰── .gitignore                          # Git ignore file
```

## Installation

1. Do Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Create a Virtual Environment:
   ```bash
   python -m venv .venv
   .venv/Scripts/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables as needed (e.g., database URL, RabbitMQ settings).

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn server.main:app --reload
   ```

2. Run the Streamlit application
   ```bash
   streamlit run client/app.py
   ```

### REST API Endpoints


| **HTTP Method** | **Endpoint**         | **Description**                                   |
|------------------|----------------------|---------------------------------------------------|
| `POST`          | `/api/register`      | Register a new user.                             |
| `POST`          | `/api/token`         | Login and obtain an access token.                |
| `GET`           | `/api/users/me`      | Retrieve the current user's profile.             |
| `PUT`           | `/api/users/me`      | Update the current user's profile.               |
| `PUT`           | `/api/users/me/password` | Update the current user's password.             |
| `DELETE`        | `/api/users/me`      | Delete the current user's account.               |

---

### GraphQL Queries

| **Query Name**             | **Description**                                      |
|-----------------------------|------------------------------------------------------|
| `hello(userId: Int!)`       | Greet a user by their ID.                            |
| `getAllTopics`              | Retrieve all topics.                                 |
| `getTopicByName(title: String!)` | Retrieve a topic by its title.                  |
| `searchTopics(prefix: String!)`  | Search for topics by a prefix.                  |
| `getTopicsByUser`           | Retrieve topics created by the current user.         |
| `getCommentsByTopicId(topicId: Int!)` | Retrieve comments for a specific topic.     |
| `getCommentsByUserId(userId: Int!)`  | Retrieve comments made by a specific user.   |
| `getTrendingTopics(timeWindow: Int, maxTopics: Int)` | Retrieve trending topics.   |
| `getUserNotifications`      | Retrieve notifications for the current user.         |

---

### GraphQL Mutations

| **Mutation Name**           | **Description**                                      |
|-----------------------------|------------------------------------------------------|
| `createTopic(title: String!, content: String!, isLocked: Boolean!)` | Create a new topic. |
| `updateTopic(topicId: Int!, title: String!, content: String!)` | Update an existing topic. |
| `deleteTopic(topicId: Int!)` | Delete a topic.                                      |
| `createComment(topicId: Int!, content: String!)` | Create a new comment on a topic. |
| `updateComment(commentId: Int!, content: String!)` | Update an existing comment.     |
| `deleteComment(commentId: Int!)` | Delete a comment.                              |
| `markNotificationRead(notificationId: Int!)` | Mark a specific notification as read. |
| `markAllNotificationsRead`  | Mark all notifications as read.                      |


## Testing

```
pytest
```
 

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any proposed changes.

## License

This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for details.
