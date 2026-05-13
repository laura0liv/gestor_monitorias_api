from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime


class SeguimientoAcademico(BaseModel):
    id_seguimiento: Optional[int] = None
    id_estudiante: int
    id_monitor: int
    id_periodo: int
    fecha_inicio: date
    nivel_riesgo: Optional[str] = None
    motivo: Optional[str] = None
    plan_acompanamiento: str
    resultado: str
    estado: str
    fecha_cierre: Optional[date] = None
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None