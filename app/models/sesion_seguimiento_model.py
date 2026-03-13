from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class SesionSeguimiento(BaseModel):
    id_sesion: Optional[int] = None
    id_seguimiento: int
    fecha: date
    observaciones: Optional[str] = None
    avance: Optional[int] = None
