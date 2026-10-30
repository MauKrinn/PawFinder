import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Annotated

from backend.core.config import settings
from backend.core.database import get_session
from backend.models.user import Usuario

security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verifica el token JWT de Supabase y extrae el UUID del usuario (sub).
    """
    token = credentials.credentials
    try:
        # Supabase firma sus JWT usando el SUPABASE_KEY (JWT Secret)
        payload = jwt.decode(
            token, 
            settings.SUPABASE_KEY, 
            algorithms=["HS256"], 
            audience="authenticated"
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no contiene un ID de usuario válido",
            )
        return user_id
    except jwt.ExpiredSignatureError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

# Dependencia para requerir que el usuario exista en la DB de SQLite
def get_current_user(
    user_id: Annotated[str, Depends(get_current_user_id)],
    session: Session = Depends(get_session)
) -> Usuario:
    """
    Busca en SQLite al usuario asociado al token validado.
    """
    statement = select(Usuario).where(Usuario.id == user_id)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no registrado en la base de datos local. Sincronice primero.",
        )
    return user