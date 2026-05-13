from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Programa(BaseModel):
    id_programa: Optional[int] = None
    nombre_programa: str
    facultad: str
    descripcion: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None