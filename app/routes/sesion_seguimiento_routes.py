from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.sesion_seguimiento_model import SesionSeguimiento
from controllers.sesion_seguimiento_controller import SesionSeguimientoController

router = APIRouter(
    prefix="/sesion_seguimiento",
    tags=["Sesion Seguimiento"]
)
nuevo_sesion_seguimiento = SesionSeguimientoController()

@router.get("/get_sesion_seguimiento/")
async def get_sesion_seguimiento():
    rpta = nuevo_sesion_seguimiento.get_all_sesion_seguimiento()
    return rpta

@router.get("/get_sesion_seguimiento/{id_sesion_seguimiento}")
async def get_sesion_seguimiento(id_sesion_seguimiento: int):
    rpta = nuevo_sesion_seguimiento.get_sesion_seguimiento(id_sesion_seguimiento)
    return rpta 

@router.post("/create_sesion_seguimiento/")
async def create_sesion_seguimiento(sesion_seguimiento: SesionSeguimiento): 
    sesion_seguimiento_data = jsonable_encoder(sesion_seguimiento)
    rpta = nuevo_sesion_seguimiento.create_sesion_seguimiento(sesion_seguimiento_data)
    return rpta

@router.put("/update_sesion_seguimiento/{id_sesion_seguimiento}")
async def update_sesion_seguimiento(id_sesion_seguimiento: int, sesion_seguimiento: SesionSeguimiento):
    sesion_seguimiento_data = jsonable_encoder(sesion_seguimiento)
    rpta = nuevo_sesion_seguimiento.update_sesion_seguimiento(id_sesion_seguimiento, sesion_seguimiento_data)
    return rpta

@router.delete("/delete_sesion_seguimiento/{id_sesion_seguimiento}")
async def delete_sesion_seguimiento(id_sesion_seguimiento: int):
    rpta = nuevo_sesion_seguimiento.delete_sesion_seguimiento(id_sesion_seguimiento)
    return rpta
