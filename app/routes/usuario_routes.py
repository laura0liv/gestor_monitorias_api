
from fastapi import APIRouter
from controllers.usuario_controller import UsuarioController
from models.usuario_model import Usuario


router = APIRouter()
nuevo_usuario = UsuarioController()

@router.get("/get_usuario/")
async def get_usuario():
    rpta = nuevo_usuario.get_all_usuario()
    return rpta

