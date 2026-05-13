from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Aula(BaseModel):
    id_aula: Optional[int] = None
    nombre_aula: str
    bloque: str
    capacidad: int
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None