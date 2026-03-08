from pydantic import BaseModel, EmailStr
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre : str
    apellido: str
    correo: EmailStr
    telefono: str
    contraseña: str
    estado: Optional[str] = "activo"
    tipo_documento: str
    numero_documento: str