from pydantic import BaseModel, EmailStr
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    tipo_documento: str
    numero_documento: str
    nombre : str
    apellido: str
    correo: EmailStr
    telefono: str
    contrasena: str
    estado: Optional[str] = "activo"
    id_rol: int

