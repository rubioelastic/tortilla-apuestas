"""
🗄️ Configuración de Base de Datos - SQLite con soporte Docker
Versión de desarrollo sin necesidad de PostgreSQL
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Base de datos SQLite para desarrollo (archivo local)
# En Docker: /app/data/tortilla_apuestas_dev.db (persistente)
# En local: ./tortilla_apuestas_dev.db
DB_PATH = os.getenv("DB_PATH", "./tortilla_apuestas_dev.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crear engine (conexión a la BD)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False  # Cambiar a True para ver las queries SQL
)

# Crear sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Crear todas las tablas
def init_db():
    """Crear todas las tablas definidas en models.py"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ Base de datos SQLite inicializada ({DB_PATH})")


# Dependency para FastAPI (inyección de sesión)
def get_db():
    """Proporciona sesión de BD para cada request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
