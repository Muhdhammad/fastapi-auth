from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    # password: str - it is better option in UserCreate

class UserCreate(UserBase):
    password: str = Field(max_length=15)

class UserLogin(BaseModel):
    identifier: str   # identifier is username or email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_verified: bool
    role: str

    class Config:
        from_attributes = True

class UserCreateResponse(BaseModel):
    message: str
    data: UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None