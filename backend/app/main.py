from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful para la plataforma web de adopción de mascotas."
)

# Configuración CORS para permitir peticiones desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se debe cambiar por el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": f"Bienvenido a la API de {settings.PROJECT_NAME}"}