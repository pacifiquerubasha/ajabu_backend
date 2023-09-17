from fastapi import FastAPI
from models import models
from lib.database import engine
from routers import users, posts, comments, friends

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(friends.router)