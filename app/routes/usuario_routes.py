
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from controllers.usuario_controller import UsuarioController
from models.usuario_model import Usuario


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)
nuevo_usuario = UsuarioController()

@router.get("/get_all_usuario/")
async def get_all_usuario():
    rpta = nuevo_usuario.get_all_usuario()
    return rpta

@router.get("/get_usuario/{id_usuario}")
async def get_usuario(id_usuario: int):
    rpta = nuevo_usuario.get_usuario(id_usuario)
    return rpta 

@router.post("/create_usuario/")
async def create_usuario(usuario: Usuario): 
    usuario_data = jsonable_encoder(usuario)
    rpta = nuevo_usuario.create_usuario(usuario_data)
    return rpta

@router.put("/update_usuario/{id_usuario}")
async def update_usuario(id_usuario: int, usuario: Usuario):
    usuario_data = jsonable_encoder(usuario)
    rpta = nuevo_usuario.update_usuario(id_usuario, usuario_data)
    return rpta

@router.delete("/delete_usuario/{id_usuario}")
async def delete_usuario(id_usuario: int):
    rpta = nuevo_usuario.delete_usuario(id_usuario)
    return rpta

@router.get("/get_users_by_role/{role_id}")
async def get_users_by_role(role_id: int):
    rpta = nuevo_usuario.get_users_by_role(role_id)
    return rpta

@router.post("/create_user_if_admin/{current_user_role}")
async def create_user_if_admin(current_user_role: int, usuario: Usuario):
    usuario_data = jsonable_encoder(usuario)
    rpta = nuevo_usuario.create_user_if_admin(current_user_role, usuario_data)
    return rpta

@router.put("/update_user_role/{current_user_role}/{id_usuario}/{new_role_id}")
async def update_user_role(current_user_role: int, id_usuario: int, new_role_id: int):
    rpta = nuevo_usuario.update_user_role(current_user_role, id_usuario, new_role_id)
    return rpta

@router.delete("/delete_user_if_admin/{current_user_role}/{id_usuario}")
async def delete_user_if_admin(current_user_role: int, id_usuario: int):
    rpta = nuevo_usuario.delete_user_if_admin(current_user_role, id_usuario)
    return rpta

