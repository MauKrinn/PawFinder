from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional

from backend.core.database import get_session
from backend.models.pet import Mascota

router = APIRouter(prefix="/pets", tags=["Mascotas"])

@router.get("/", response_model=List[Mascota])
def get_pets(
    session: Session = Depends(get_session),
    especie: Optional[str] = None,
    tamano: Optional[str] = None,
    edad: Optional[str] = None,
    convive_ninos: Optional[str] = None,
    convive_perros: Optional[str] = None,
    convive_gatos: Optional[str] = None,
):
    """
    Obtiene el catálogo público de mascotas.
    Aplica filtros dinámicos basados en los parámetros de la URL.
    Solo devuelve mascotas en estado 'ACTIVA'.
    """
    statement = select(Mascota).where(Mascota.estado_publicacion == "ACTIVA")
    
    if especie:
        statement = statement.where(Mascota.especie == especie.upper())
    if tamano:
        statement = statement.where(Mascota.tamano == tamano.upper())
    if edad:
        statement = statement.where(Mascota.edad == edad.upper())
        
    # Filtros de convivencia (Intersección: si piden SI, exigimos SI)
    if convive_ninos:
        statement = statement.where(Mascota.convive_ninos == convive_ninos.upper())
    if convive_perros:
        statement = statement.where(Mascota.convive_perros == convive_perros.upper())
    if convive_gatos:
        statement = statement.where(Mascota.convive_gatos == convive_gatos.upper())
        
    mascotas = session.exec(statement).all()
    return mascotas