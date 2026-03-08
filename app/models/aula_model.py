from typing import Optional
from pydantic import BaseModel

class Aula(BaseModel):
    id_aula: Optional[int] = None
    nombre_aula: str
    bloque: str
    capacidad: int