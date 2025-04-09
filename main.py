from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from contextlib import asynccontextmanager
from routes.products_routes import router as products_router
from utils.routes_manager import print_routes

# Definimos la función lifespan de manera correcta
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Servidor corriendo")
    yield  # Aquí es donde FastAPI espera que "lances" el control, manteniendo la conexión abierta
    print("Servidor apagado")

# Creamos la aplicación FastAPI pasando la función lifespan correctamente
app = FastAPI(lifespan=lifespan)

# documentación de rutas
@app.get('/routes', response_class=HTMLResponse)
async def shor_routes():
    table = print_routes(app)

    return HTMLResponse(content=f"<html><body><pre>{table}</pre></body></html>")

# implementacion de routes
app.include_router(products_router, prefix="/api/products")

if __name__ == "__main__":
    # Asegúrate de levantar el servidor en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8005) 
