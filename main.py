from fastapi import FastAPI
from models import models
from lib.database import engine
from routers import users

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(users.router)