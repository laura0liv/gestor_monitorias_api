
from typing import Optional
from pydantic import BaseModel

class Programa(BaseModel):
    id_programa: Optional[int] = None
    nombre_programa: str
    facultad: str
    descripcion: str