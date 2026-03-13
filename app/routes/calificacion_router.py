from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.calificacion_model import Calificacion
from controllers.calificacion_controller import CalificacionController


router = APIRouter(
    prefix="/calificacion",
    tags=["Calificacion"]
)
nuevo_calificacion = CalificacionController()


@router.get("/get_calificaciones/")
async def get_calificaciones():
    rpta = nuevo_calificacion.get_all_calificacions()
    return rpta
@router.get("/get_calificacion/{id_calificacion}")
async def get_calificacion(id_calificacion: int):
    rpta = nuevo_calificacion.get_calificacion(id_calificacion  )
    return rpta 
@router.post("/create_calificacion/")
async def create_calificacion(calificacion: Calificacion):  
    calificacion_data = jsonable_encoder(calificacion)
    rpta = nuevo_calificacion.create_calificacion(calificacion_data)
    return rpta
@router.put("/update_calificacion/{id_calificacion}")       
async def update_calificacion(id_calificacion: int, calificacion: Calificacion):
    calificacion_data = jsonable_encoder(calificacion)
    rpta = nuevo_calificacion.update_calificacion(id_calificacion, calificacion_data)
    return rpta
@router.delete("/delete_calificacion/{id_calificacion}")
async def delete_calificacion(id_calificacion: int):
    rpta = nuevo_calificacion.delete_calificacion(id_calificacion)
    return rpta