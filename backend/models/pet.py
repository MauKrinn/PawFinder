import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Mascota(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=50)
    especie: str  # PERRO, GATO
    sexo: str  # MACHO, HEMBRA
    edad: str  # CACHORRO, ADULTO_JOVEN, ADULTO_MAYOR
    tamano: str  # PEQUENO, MEDIANO, GRANDE
    localidad: str = Field(max_length=100)
    caracter: Optional[str] = Field(default=None, max_length=100)
    
    # Convivencia
    convive_ninos: str  # SI, NO, DESCONOCIDO
    convive_perros: str  # SI, NO, DESCONOCIDO
    convive_gatos: str  # SI, NO, DESCONOCIDO
    obs_convivencia: Optional[str] = Field(default=None, max_length=250)
    
    # Salud
    estado_vacunacion: str  # AL_DIA, INCOMPLETO, SIN_VACUNAR, DESCONOCIDO
    cartilla_url: Optional[str] = None
    esterilizado: str  # SI, NO_MENOR_5_MESES, NO_MAYOR_5_MESES
    # CAMBIO: Se elimina desparasitacion_fecha y se agrega desparasitado
    desparasitado: str # SI, NO, DESCONOCIDO 
    tratamiento_especial: Optional[str] = Field(default=None, max_length=300)
    
    descripcion_historia: Optional[str] = None
    estado_publicacion: str  # BORRADOR, ACTIVA, ADOPTADA, DADA_DE_BAJA
    
    # Clave Foránea
    usuario_creador_id: uuid.UUID = Field(foreign_key="usuario.id")
    
    # Relaciones
    creador: "Usuario" = Relationship(back_populates="mascotas")
    historial: List["HistorialPublicacion"] = Relationship(back_populates="mascota")
    # CAMBIO: La relación vacunas ya es opcional (puede ser una lista vacía [])
    vacunas: List["Vacuna"] = Relationship(back_populates="mascota")