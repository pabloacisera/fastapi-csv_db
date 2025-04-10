from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.database import engine, get_db, Base
from routes.products_routes import router as products_router
from routes.user_routes import router as users_router
from routes.auth_routes import router as auth_router
from utils.routes_manager import print_routes

# Definimos la función lifespan de manera correcta
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar (si no existen)
    Base.metadata.create_all(bind=engine)

    if engine is not None:
        print("Servidor corriendo con conexion a base de Datos sqlite")
    else:
        print("Servidor ejecutado sin base de datos")
    yield  # Aquí es donde FastAPI espera que "lances" el control, manteniendo la conexión abierta
    print("Servidor apagado")

# Creamos la aplicación FastAPI pasando la función lifespan correctamente
app = FastAPI(lifespan=lifespan)

# Configuración CORS (Añade esto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # O ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# documentación de rutas
@app.get('/routes', response_class=HTMLResponse)
async def shor_routes():
    table = print_routes(app)

    return HTMLResponse(content=f"<html><body><pre>{table}</pre></body></html>")

# implementacion de routes
app.include_router(products_router, prefix="/api/products")
app.include_router(users_router, prefix="/api/users")
app.include_router(auth_router, prefix="/api/auth")

if __name__ == "__main__":
    # Asegúrate de levantar el servidor en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8005) 
