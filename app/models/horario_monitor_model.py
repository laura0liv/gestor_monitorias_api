# models/horario_monitor_model.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, time

class HorarioMonitor(BaseModel):
    id_horario: Optional[int] = None
    id_monitor: int
    dia_semana: str
    hora_inicio: str = "00:00:00"  # se guarda como string, psycopg2 lo castea a TIME
    hora_fin: str = "00:00:00"   # ← tres componentes para TIME de postgres
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None