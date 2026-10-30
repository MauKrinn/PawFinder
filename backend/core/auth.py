from fastapi import Depends, HTTPException, status
import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Annotated
from supabase import create_client, Client

from backend.core.config import settings
from backend.core.database import get_session
from backend.models.user import Usuario

security = HTTPBearer()

# Inicializamos el cliente oficial de Supabase
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verifica el token JWT enviándolo a Supabase para su validación oficial.
    """
    token = credentials.credentials
    try:
        # Le pedimos a Supabase que valide el token por nosotros
        user_res = supabase.auth.get_user(token)
        
        if not user_res or not user_res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no contiene un ID de usuario válido",
            )
        return user_res.user.id
    except Exception as e:
        print(f"❌ Error de Supabase al validar token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

# Dependencia para requerir que el usuario exista en la DB local
def get_current_user(
    user_id: Annotated[str, Depends(get_current_user_id)],
    session: Session = Depends(get_session)
) -> Usuario:
    """
    Busca en SQLite al usuario asociado al token validado.
    """
    # Convertimos el string a un objeto UUID de Python
    statement = select(Usuario).where(Usuario.id == uuid.UUID(user_id))
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no registrado en la base de datos local. Sincronice primero.",
        )
    return user