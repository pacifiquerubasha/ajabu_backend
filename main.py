from fastapi import FastAPI, Request, Depends
from models import models, schemas
from lib.database import engine
from routers import users, posts, comments, friends, auth
from lib import oauth2

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(friends.router)
app.include_router(auth.router)