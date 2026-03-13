
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from controllers.rol_controller import RolController
from models.rol_model import Rol


router = APIRouter(
    prefix="/rol",
    tags=["Rol"]
)
nuevo_rol = RolController()

@router.get("/get_rol/")
async def get_rol():
    rpta = nuevo_rol.get_all_rol()
    return rpta

@router.get("/get_rol/{id_rol}")
async def get_rol(id_rol: int): 
    rpta = nuevo_rol.get_rol(id_rol)
    return rpta

@router.post("/create_rol/")
async def create_rol(rol: Rol): 
    rol_data = jsonable_encoder(rol)
    rpta = nuevo_rol.create_rol(rol_data)
    return rpta

@router.put("/update_rol/{id_rol}")
async def update_rol(id_rol: int, rol: Rol):
    rol_data = jsonable_encoder(rol)
    rpta = nuevo_rol.update_rol(id_rol, rol_data)
    return rpta

@router.delete("/delete_rol/{id_rol}")
async def delete_rol(id_rol: int):
    rpta = nuevo_rol.delete_rol(id_rol)
    return rpta