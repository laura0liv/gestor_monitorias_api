from typing import Optional
from pydantic import BaseModel

class HorarioMonitor(BaseModel):
    id_horario_monitor: Optional[int] = None
    id_monitor: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str
 