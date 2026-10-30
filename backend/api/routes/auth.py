import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated

from backend.core.database import get_session
from backend.core.auth import get_current_user_id
from backend.models.user import Usuario
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class SyncUserRequest(BaseModel):
    email: str
    nombre: str
    whatsapp: str

@router.post("/sync", status_code=status.HTTP_200_OK)
def sync_user(
    sync_data: SyncUserRequest,
    user_id_str: Annotated[str, Depends(get_current_user_id)],
    session: Session = Depends(get_session)
):
    """
    Verifica si el usuario autenticado en Supabase ya existe en SQLite.
    Si no existe, lo inserta utilizando los datos proporcionados por el frontend.
    """
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
         raise HTTPException(status_code=400, detail="El ID del token no es un UUID válido")

    # Verifica si ya existe
    statement = select(Usuario).where(Usuario.id == user_uuid)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        return {"message": "Usuario ya sincronizado", "user": existing_user}
    
    # Si no existe, lo creamos
    new_user = Usuario(
        id=user_uuid,
        email=sync_data.email,
        nombre=sync_data.nombre,
        whatsapp=sync_data.whatsapp
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "Usuario registrado exitosamente en la base de datos local", "user": new_user}