from typing import List, Optional
from pydantic import BaseModel

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

