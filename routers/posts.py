from fastapi import APIRouter, Depends, HTTPException, status
from lib import database, oauth2
from models import schemas, models
from sqlalchemy.orm import Session


from typing import List

# import cloudinary
# import cloudinary.uploader

from dotenv import load_dotenv
import os

load_dotenv()

# cloudinary.config(
#     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.getenv("CLOUDINARY_API_KEY"),
#     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# )


router = APIRouter(
    prefix="/api/v1/posts",
    tags=["posts"]
)

get_db = database.get_db

@router.post("/", response_model=schemas.PostSchema)
def create_post(request:schemas.PostSchema, db: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    
    #Check if user exists
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_post = models.Post(**request.__dict__)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/", response_model=List[schemas.PostResponseSchema])
def get_all_posts(db: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    
    return posts

@router.get("/{id}", response_model=schemas.PostResponseSchema)
def get_post(id:int, db: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post


@router.get("/search/{user_id}", response_model= List[schemas.PostResponseSchema])
def get_user_posts(user_id:int, db:Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter_by(user_id=user_id).all()
    
    return posts