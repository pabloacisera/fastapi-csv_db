from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.User import User
from database.database import Base, get_db, engine
from schemas.UserSchema import UserRead, UserCreate
from utils.auth import hash_password

# crea la tabla users en la db conectada a través de engine
Base.metadata.create_all(bind=engine)

router = APIRouter()

# la respuesta va a seguir el schema UserRead
@router.post('/', response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # verificar si el mail existe
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')

    # convierte el schema a dict
    db_user = User(
        name = user.name,
        username = user.username,
        email = user.email,
        password = hash_password(user.password),
        role = user.role
    )

    # agrega el nuevo usuario a la sesion
    db.add(db_user)

    #confirma la transacción
    db.commit()

    # actualiza la instancia
    db.refresh(db_user)

    return db_user