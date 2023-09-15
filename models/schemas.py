from typing import List, Optional
from pydantic import BaseModel
from fastapi import UploadFile

"""
User schema 
"""
class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str

    class Config():
        orm_mode = True

"""
User response schema 
"""
class UserResponseSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    profile_picture: Optional[str]
    is_verified:bool
    verification_code: Optional[str]


    class Config():
        orm_mode = True


"""
Posts schema
"""
class PostSchema(BaseModel):
    title:str
    body:str
    image:Optional[UploadFile]
    user_id:int

    class Config():
        orm_mode = True

"""
Post response schema
"""
class PostResponseSchema(BaseModel):
    title:str
    body:str
    image:Optional[str]
    user: UserResponseSchema

    class Config():
        orm_mode = True

"""
Comments schema
"""
class CommentSchema(BaseModel):
    body:str
    user_id:int
    post_id:int

    class Config():
        orm_mode = True

"""
Comments response schema
"""

class CommentResponseSchema(BaseModel):
    body:str
    user: UserResponseSchema
    post_id: int

    class Config():
        orm_mode = True