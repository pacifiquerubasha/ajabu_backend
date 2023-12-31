from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from models import schemas, models
from lib import database, token, hashing

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Auth"]
)

get_db = database.get_db
Hash = hashing.Hash

@router.post('/login')
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    #Check that user.is_verified
    # if user.is_verified == "0":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not verified. Please check your email")

    access_token = token.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer", "user": user}