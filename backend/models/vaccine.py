import uuid
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Vacuna(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    mascota_id: uuid.UUID = Field(foreign_key="mascota.id")
    nombre: str
    fecha: date
    
    # Relación
    mascota: "Mascota" = Relationship(back_populates="vacunas")