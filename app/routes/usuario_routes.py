
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from controllers.usuario_controller import UsuarioController
from models.usuario_model import Usuario


router = APIRouter()
nuevo_usuario = UsuarioController()

@router.get("/get_usuario/")
async def get_usuario():
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
