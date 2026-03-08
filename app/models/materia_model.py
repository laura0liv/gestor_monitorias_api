from typing import Optional
from pydantic import BaseModel

class Materia(BaseModel):
    id_materia: Optional[int] = None
    nombre_materia: str
    codigo_materia: str
    creditos: int
    id_programa: int