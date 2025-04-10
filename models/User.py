from sqlalchemy import Column, Integer, String, Enum
from database.database import Base
import enum


class Role(enum.Enum):
    admin='admin'
    user='user'
    guest='guest'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    username = Column(String(150))
    email = Column(String(255), index=True, unique=True)  # Cambio importante aquí
    password = Column(String(50))
    role = Column(Enum(Role), default=Role.user)