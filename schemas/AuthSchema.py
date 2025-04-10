from typing import Optional
from pydantic import BaseModel, EmailStr
import enum

# Definimos Role aquí para evitar importación circular
class Role(str, enum.Enum):
    admin = 'admin'
    user = 'user'
    guest = 'guest'

class AuthSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Valor por defecto

class TokenData(BaseModel):
    email: Optional[str] = None

# Schema básico para datos de usuario en respuesta de login
class UserLoginInfo(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    role: Role

class LoginResponse(BaseModel):
    user: UserLoginInfo
    token: Token