from supabase import create_client, Client
from fastapi import UploadFile, HTTPException
import uuid
import os

from backend.core.config import settings

# Inicializamos el cliente de Supabase
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Nombre del bucket que debes crear en tu panel de Supabase
BUCKET_NAME = "mascotas-imagenes"

async def upload_image_to_supabase(file: UploadFile) -> str:
    """
    Sube una imagen al bucket público de Supabase Storage y retorna su URL.
    """
    # Validaciones básicas
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido. Usa JPG, PNG o WEBP.")
    
    if file.size > 5 * 1024 * 1024:  # 5 MB limit
        raise HTTPException(status_code=400, detail="La imagen no debe superar los 5MB.")

    try:
        # Leemos el archivo en memoria
        file_bytes = await file.read()
        
        # Generamos un nombre único para evitar colisiones
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Subimos a Supabase
        res = supabase.storage.from_(BUCKET_NAME).upload(
            file=file_bytes,
            path=unique_filename,
            file_options={"content-type": file.content_type}
        )
        
        # Obtenemos la URL pública
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
        return public_url
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {str(e)}")