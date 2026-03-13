
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.monitoria_model import Monitoria
from controllers.monitoria_controller import MonitoriaController

router = APIRouter(
    prefix="/monitoria",
    tags=["Monitoria"]
)
nueva_monitoria = MonitoriaController()

@router.get("/get_all_monitoria/")
async def get_all_monitorias():
    rpta = nueva_monitoria.get_all_monitorias()
    return rpta

@router.get("/get_monitoria/{id_monitoria}")
async def get_monitoria(id_monitoria: int): 
    rpta = nueva_monitoria.get_monitoria(id_monitoria)
    return rpta

@router.post("/create_monitoria/")
async def create_monitoria(monitoria: Monitoria): 
    monitoria_data = jsonable_encoder(monitoria)
    rpta = nueva_monitoria.create_monitoria(monitoria_data)
    return rpta

@router.put("/update_monitoria/{id_monitoria}")
async def update_monitoria(id_monitoria: int, monitoria: Monitoria):
    monitoria_data = jsonable_encoder(monitoria)
    rpta = nueva_monitoria.update_monitoria(id_monitoria, monitoria_data)
    return rpta

@router.delete("/delete_monitoria/{id_monitoria}")
async def delete_monitoria(id_monitoria: int):
    rpta = nueva_monitoria.delete_monitoria(id_monitoria)
    return rpta