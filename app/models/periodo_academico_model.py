from pydantic import BaseModel
from typing import Optional
from datetime import date

class PeriodoAcademico(BaseModel):
    id_periodo: Optional[int] = None
    nombre_periodo: str
    fecha_inicio: date
    fecha_fin: date
    estado: str