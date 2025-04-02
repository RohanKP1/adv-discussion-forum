# Adv Real-Time Discussion Forum

This project is an implementation of a web application using FastAPI and GraphQL, with support for user authentication, notifications via RabbitMQ, and data storage using SQLAlchemy.

## Features

- User Registration and Authentication
- Topic and Comment Management
- Notification System using RabbitMQ
- GraphQL API with Mutations and Queries
- Database Integration with SQLAlchemy

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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
