from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Rol(BaseModel):
    id_rol: Optional[int] = None
    nombre_rol: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
