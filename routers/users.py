from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import schemas, models
from lib import database

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

get_db = database.get_db

@router.post("/")
def createUser(request: schemas.UserSchema, db: Session = Depends(get_db)):
    
    return "success"
