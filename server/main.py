import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.src.api.login import app as login_app
from server.src.graphql.gql import app as graphql_app
# from server.src.db.populate import populate_main
# from server.src.rabbitmq.rmq import rmq_main
# from server.src.rabbitmq.notification import example_notification_workflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", login_app)
app.mount("/graphql", graphql_app)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # populate_main()
    # rmq_main()
    # example_notification_workflow()

