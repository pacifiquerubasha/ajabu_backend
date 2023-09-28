from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import schemas, models
from lib import database, hashing
from typing import List

from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

get_db = database.get_db
Hash = hashing.Hash

conf = ConnectionConfig(
   MAIL_SERVER=str(os.getenv("EMAIL_HOST")),
   MAIL_PORT=int(os.getenv("EMAIL_PORT")),
   MAIL_USERNAME=str(os.getenv("EMAIL_USERNAME")),
   MAIL_PASSWORD=str(os.getenv("EMAIL_PASSWORD")),
   MAIL_FROM = "test@ajabu.com",
   MAIL_STARTTLS = False,
   MAIL_SSL_TLS = False,
   USE_CREDENTIALS = True,
   VALIDATE_CERTS = True
)

async def send_mail(email: schemas.EmailSchema):
 
    template = """
        <html>
        <body>
         
 
<p>Hi !!!
        <br>Thanks for using fastapi mail, keep using it..!!!</p>
 
 
        </body>
        </html>
        """
 
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=template,
        subtype="html"
        )
 
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)
 
     
 
    return {"message": "email has been sent"}

# @router.post("/", response_model=schemas.UserResponseSchema)
@router.post("/")
async def createUser(request: schemas.UserSchema, db: Session = Depends(get_db)):

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

    #Send email
    email = schemas.EmailSchema(email=[request.email])
    await send_mail(email)
    
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