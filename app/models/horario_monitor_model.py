from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class HorarioMonitor(BaseModel):
    id_horario_monitor: Optional[int] = None
    id_monitor: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
 