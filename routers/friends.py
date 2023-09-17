from models import schemas, models
from lib import database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter(
    prefix="/api/v1/friends",
    tags=["friends"]
)

get_db = database.get_db


@router.post("/", response_model=schemas.FriendsResponseSchema)
# @router.post("/")
def create_friend(request:schemas.FriendsSchema, db: Session = Depends(get_db)):
        
        #Check if user exists
        user = db.query(models.User).filter(models.User.id == request.friend_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        #Check if friendship exists
        friendship = db.query(models.Friend).filter_by(user_id = request.user_id, friend_id = request.friend_id).first()
        if friendship:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You already have this user as a friend")
    
        new_friend = models.Friend(**request.__dict__)
        db.add(new_friend)
        db.commit()
        db.refresh(new_friend)
    
        return new_friend

"""
    GET ALL CONFIRMED FRIENDSHIPS
"""
@router.get("/{user_id}", response_model=List[schemas.FriendsResponseSchema])
def get_friends(user_id:int, db: Session = Depends(get_db)):
    friends = db.query(models.Friend).filter_by(user_id = user_id, status=2).all()
    if not friends:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No friends found")
    
    return friends

"""
    GET PENDING REQUESTS SENT BY ME
"""
@router.get("/{user_id}", response_model=List[schemas.FriendsResponseSchema])
def get_friend_requests(user_id:int, db: Session = Depends(get_db)):
    friends = db.query(models.Friend).filter_by(user_id = user_id, status=1).all()
    if not friends:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No friend requests found")
    
    return friends


"""
    GET PENDING REQUESTS SENT TO ME
"""
@router.get("/{user_id}", response_model=List[schemas.FriendsResponseSchema])
def get_friend_requests(user_id:int, db: Session = Depends(get_db)):
    friends = db.query(models.Friend).filter_by(friend_id = user_id, status=1).all()
    if not friends:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No friend requests found")
    
    return friends


"""
    UPDATE FRIENDSHIP STATUS
"""
@router.put("/{user_id}/{friend_id}", response_model=schemas.FriendsResponseSchema)
def confirm_friendship(user_id:int, friend_id:int, request:schemas.FriendShipStatusChangeSchema, db: Session = Depends(get_db)):
    friendship = db.query(models.Friend).filter_by(user_id = user_id, friend_id = friend_id).first()
    if not friendship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")
    
    friendship.status = request.status
    db.commit()
    db.refresh(friendship)
    
    return friendship