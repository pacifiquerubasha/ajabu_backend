from fastapi import APIRouter, Depends, HTTPException, status
from lib import database
from models import schemas, models
from sqlalchemy.orm import Session

from typing import List
router = APIRouter(
    prefix="/api/v1/comments",
    tags=["comments"]
)

get_db = database.get_db

@router.post("/", response_model=schemas.CommentSchema)
def create_comment(request:schemas.CommentSchema, db:Session=Depends(get_db)):
        
        #Check if user exists
        user = db.query(models.User).filter(models.User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        #Check if post exists
        post = db.query(models.Post).filter(models.Post.id == request.post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
        new_comment = models.Comment(**request.__dict__)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    
        return new_comment


@router.get("/{post_id}", response_model=List[schemas.CommentResponseSchema])
def get_comments(post_id:int, db:Session=Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    
    return comments