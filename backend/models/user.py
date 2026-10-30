import uuid
from typing import List
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    nombre: str
    whatsapp: str
    
    # Relación uno a muchos con mascotas
    mascotas: List["Mascota"] = Relationship(back_populates="creador")