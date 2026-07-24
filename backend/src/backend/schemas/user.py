from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email : EmailStr
    username : str = Field(min_length=3,max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime