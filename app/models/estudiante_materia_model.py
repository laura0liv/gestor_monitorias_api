from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class EstudianteMateria(BaseModel):
    id_estudiante: Optional[int] = None
    id_materia: int
    id_periodo: int
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None