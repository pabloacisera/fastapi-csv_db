# /database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.environments import sqlite_uri

Base = declarative_base()

# Define la URL de la base de datos globalmente
SQLALCHEMY_DATABASE_URL = sqlite_uri


# Crea el motor de la base de datos una sola vez
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
    print("Conexión a la base de datos establecida.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    engine = None  # Importante para manejar el caso de fallo

# Crea la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()