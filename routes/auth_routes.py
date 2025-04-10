from datetime import timedelta
from fastapi.security import HTTPBearer
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from config.environments import ACCESS_TOKEN_EXPIRES
from models.User import User
from database.database import get_db
from schemas.AuthSchema import AuthSchema, LoginResponse, UserLoginInfo, Token
from utils.auth import verify_password, create_access_token

router = APIRouter()
security = HTTPBearer()

@router.post('/login', response_model=LoginResponse, status_code=200)
async def login(response: Response, user: AuthSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='El correo electronico no existe en base de datos')

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El password no es correcto o no existe')

    # crear token de acceso
    token_expires_minutes = int(ACCESS_TOKEN_EXPIRES)
    access_token_expires = timedelta(minutes=token_expires_minutes)
    access_token = create_access_token(
        data= { "sub": db_user.email },
        expires_delta=access_token_expires
    )

    # config cookie HTTP-Only segura
    response.set_cookie(
        key='access_token',
        value=f'Bearer {access_token}',
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRES * 60,
        secure=False, #True en producción: solo envia cookie sobre HTTPS
        samesite= 'lax',
        path='/'
    )

    user_data = {
        "id": db_user.id,
        "name": db_user.name,
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role.value # .value para el enum
    }

    return LoginResponse(
        user=UserLoginInfo(
            id=db_user.id,
            name=db_user.name,
            username=db_user.username,
            email=db_user.email,
            role=db_user.role.value
        ),
        token=Token(
            access_token=access_token
        )
    )

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {
        "message":"Logged out successfully"
    }