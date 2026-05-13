from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MonitorMateria(BaseModel):
    id_monitor: int
    id_materia: int
