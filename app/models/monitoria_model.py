from typing import Optional
from pydantic import BaseModel
from datetime import date

class Monitoria(BaseModel):
    id_monitoria: Optional[int] = None
    id_monitor: int
    id_estudiante: int
    id_materia: int
    id_aula: int
    fecha: date
    hora_inicio: str
    hora_fin: str
    modalidad: str
    estado: str
    id_periodo: int
    asistencia: Optional[bool] = None
    observaciones: Optional[str] = None
