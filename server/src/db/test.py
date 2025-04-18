from sqlalchemy import inspect
from server.src.db.session import engine

def check_tables_exist():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected_tables = ['users', 'topics', 'comments', 'notifications', 'user_topic_subscriptions', 'tags', 'topic_tags']
    
    for table in expected_tables:
        if table in tables:
            print(f"Table '{table}' exists.")
        else:
            print(f"Table '{table}' does not exist.")

if __name__ == "__main__":
    check_tables_exist()