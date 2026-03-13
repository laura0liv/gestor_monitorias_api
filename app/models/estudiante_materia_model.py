from typing import Optional
from pydantic import BaseModel

class EstudianteMateria(BaseModel):
    id_estudiante: Optional[int] = None
    id_materia: int
    id_periodo: int