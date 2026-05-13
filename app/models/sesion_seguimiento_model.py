from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class SesionSeguimiento(BaseModel):
    id_sesion: Optional[int] = None
    id_seguimiento: int
    fecha: date
    observaciones: Optional[str] = None
    avance: Optional[int] = None
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None