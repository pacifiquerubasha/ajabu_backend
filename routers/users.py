from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import schemas, models
from lib import database, hashing
from typing import List

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

get_db = database.get_db
Hash = hashing.Hash

@router.post("/", response_model=schemas.UserResponseSchema)
def createUser(request: schemas.UserSchema, db: Session = Depends(get_db)):

    #Check if user exists
    user = db.query(models.User).filter_by(username = request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    #Hash password
    request.password = Hash.encrypt(request.password)

    newuser = models.User(**request.__dict__)
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    
    return newuser


@router.get("/{username}", response_model=schemas.UserResponseSchema)
def getUser(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=List[schemas.UserResponseSchema])
def getUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users