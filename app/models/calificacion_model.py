from typing import Optional
from pydantic import BaseModel

class Calificacion(BaseModel):
    id_calificacion: Optional[int] = None
    id_monitoria: int
    puntuacion: int
    comentario: str
    fecha_calificacion: str