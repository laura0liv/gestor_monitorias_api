
from typing import Optional
from pydantic import BaseModel

class Rol(BaseModel):
    id_rol: Optional[int] = None
    nombre_rol: str
