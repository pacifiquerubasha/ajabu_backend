from typing import List, Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    """User schema."""
    username:str