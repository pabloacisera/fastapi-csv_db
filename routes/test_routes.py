from fastapi import APIRouter
from fastapi.responses import JSONResponse 

router = APIRouter()

@router.get('/welcome/{name}', response_description='sample saludations')
async def welcome(name: str):
    return {
        JSONResponse(status_code=200, content=f'Bienvenido a nuestra app {name}')
    }
