from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class Role(str, enum.Enum):
    admin='admin'
    user='user'
    guest='guest'

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: Optional[Role] = Role.user

class UserRead(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes=True
        json_encoders= {
            enum.Enum: lambda v: v.value
        }

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None