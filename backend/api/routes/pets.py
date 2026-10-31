from fastapi import APIRouter, Depends, Query, Form, UploadFile, File, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import BaseModel
import uuid

from backend.core.database import get_session
from backend.models.pet import Mascota
from backend.models.user import Usuario
from backend.core.auth import get_current_user
from backend.services.storage import upload_image_to_supabase

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
    """Obtiene el catálogo público de mascotas."""
    statement = select(Mascota).where(Mascota.estado_publicacion == "ACTIVA")
    
    if especie:
        statement = statement.where(Mascota.especie == especie.upper())
    if tamano:
        statement = statement.where(Mascota.tamano == tamano.upper())
    if edad:
        statement = statement.where(Mascota.edad == edad.upper())
    if convive_ninos:
        statement = statement.where(Mascota.convive_ninos == convive_ninos.upper())
    if convive_perros:
        statement = statement.where(Mascota.convive_perros == convive_perros.upper())
    if convive_gatos:
        statement = statement.where(Mascota.convive_gatos == convive_gatos.upper())
        
    return session.exec(statement).all()


@router.post("/", response_model=Mascota)
async def create_pet(
    # El candado: exige que el usuario esté logueado y registrado
    current_user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session),
    
    # Campos del formulario
    nombre: str = Form(...),
    especie: str = Form(...),
    sexo: str = Form(...),
    edad: str = Form(...),
    tamano: str = Form(...),
    localidad: str = Form(...),
    convive_ninos: str = Form(...),
    convive_perros: str = Form(...),
    convive_gatos: str = Form(...),
    estado_vacunacion: str = Form(...),
    esterilizado: str = Form(...),
    desparasitado: str = Form(...),
    
    # Opcionales
    caracter: Optional[str] = Form(None),
    obs_convivencia: Optional[str] = Form(None),
    tratamiento_especial: Optional[str] = Form(None),
    descripcion_historia: Optional[str] = Form(None),
    
    # Imagen obligatoria
    foto: UploadFile = File(...)
):
    """Crea una nueva mascota (Requiere autenticación)."""
    
    # 1. Subimos la foto a Supabase Storage
    imagen_url = await upload_image_to_supabase(foto)
    
    # 2. Creamos el registro en SQLite
    nueva_mascota = Mascota(
        nombre=nombre,
        especie=especie.upper(),
        sexo=sexo.upper(),
        edad=edad.upper(),
        tamano=tamano.upper(),
        localidad=localidad,
        caracter=caracter,
        convive_ninos=convive_ninos.upper(),
        convive_perros=convive_perros.upper(),
        convive_gatos=convive_gatos.upper(),
        obs_convivencia=obs_convivencia,
        estado_vacunacion=estado_vacunacion.upper(),
        esterilizado=esterilizado.upper(),
        desparasitado=desparasitado.upper(),
        tratamiento_especial=tratamiento_especial,
        descripcion_historia=descripcion_historia,
        estado_publicacion="ACTIVA", # Por defecto entra activa al catálogo
        cartilla_url=imagen_url, # Usamos este campo provisionalmente para la foto principal
        usuario_creador_id=current_user.id
    )
    
    session.add(nueva_mascota)
    session.commit()
    session.refresh(nueva_mascota)
    
    return nueva_mascota

# Esquema para recibir solo el campo de estado
class MascotaUpdate(BaseModel):
    estado_publicacion: str

@router.patch("/{pet_id}", response_model=Mascota)
def update_pet_status(
    pet_id: uuid.UUID,
    pet_update: MascotaUpdate,
    current_user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Actualiza el estado de una mascota (Ej: de ACTIVA a ADOPTADA). Solo el creador puede hacerlo."""
    mascota = session.get(Mascota, pet_id)
    
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
        
    # Validamos que quien intenta modificar sea el dueño de la publicación
    if mascota.usuario_creador_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esta mascota"
        )
        
    mascota.estado_publicacion = pet_update.estado_publicacion.upper()
    session.add(mascota)
    session.commit()
    session.refresh(mascota)
    
    return mascota


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
    pet_id: uuid.UUID,
    current_user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Elimina físicamente un expediente del sistema. Solo el creador puede hacerlo."""
    mascota = session.get(Mascota, pet_id)
    
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
        
    # Validamos que quien intenta eliminar sea el dueño de la publicación
    if mascota.usuario_creador_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para eliminar esta mascota"
        )
        
    session.delete(mascota)
    session.commit()
    return