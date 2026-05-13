from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Materia(BaseModel):
    id_materia: Optional[int] = None
    nombre_materia: str
    codigo_materia: str
    creditos: int
    id_programa: int
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None