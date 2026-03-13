from typing import Optional
from pydantic import BaseModel

class MonitorMateria(BaseModel):
    id_monitor: Optional[int] = None
    id_materia: int
