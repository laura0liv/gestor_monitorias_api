from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Calificacion(BaseModel):
    id_calificacion: Optional[int] = None
    id_monitoria: int
    puntuacion: int
    comentario: str
    fecha_calificacion: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
