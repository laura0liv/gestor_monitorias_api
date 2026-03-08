from typing import Optional
from pydantic import BaseModel

class Monitoria(BaseModel):
    id_monitoria: Optional[int] = None
    id_monitor: int
    id_estudiante: int
    id_materia: int
    id_aula: int
    fecha: str
    hora_inicio: str
    hora_fin: str
    modalidad: str
    estado: str
