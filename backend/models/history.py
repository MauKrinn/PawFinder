import uuid
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class HistorialPublicacion(SQLModel, table=True):
    __tablename__ = "historial_publicacion"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    mascota_id: uuid.UUID = Field(foreign_key="mascota.id")
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tipo_evento: str  # DEVOLUCION, BAJA, ADOPCION, REACTIVACION
    estado_previo: str
    estado_nuevo: str
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    
    # Relación
    mascota: "Mascota" = Relationship(back_populates="historial")