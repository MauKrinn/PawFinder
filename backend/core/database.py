from sqlmodel import create_engine, Session
from backend.core.config import settings

# Argumento crítico para que SQLite funcione bien con el asincronismo y multithreading de FastAPI
connect_args = {"check_same_thread": False}

# echo=True imprimirá las consultas SQL en la consola para facilitar el debug en desarrollo
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args=connect_args
)

def get_session():
    """
    Dependencia de FastAPI para obtener la sesión de la base de datos.
    Garantiza que la sesión se cierre al finalizar la petición.
    """
    with Session(engine) as session:
        yield session