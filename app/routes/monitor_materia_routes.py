
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from controllers.monitor_materia_controller import MonitorMateriaController
from models.materia_model import Materia


router = APIRouter(
    prefix="/monitor_materia",
    tags=["Monitor Materia"]
)
nueva_monitor_materias = MonitorMateriaController()

@router.get("/get_monitor_materias/")
async def get_monitor_materias():
    rpta = nueva_monitor_materias.get_all_monitor_materias()
    return rpta

@router.get("/get_monitor_materia/{id_materia}")
async def get_monitor_materia(id_materia: int): 
    rpta = nueva_monitor_materias.get_monitor_materia(id_materia)
    return rpta

@router.post("/create_monitor_materia/")
async def create_monitor_materia(materia: Materia): 
    materia_data = jsonable_encoder(materia)
    rpta = nueva_monitor_materias.create_monitor_materia(materia_data)
    return rpta

@router.put("/update_monitor_materia/{id_materia}")
async def update_monitor_materia(id_materia: int, materia: Materia):
    materia_data = jsonable_encoder(materia)
    rpta = nueva_monitor_materias.update_monitor_materia(id_materia, materia_data)
    return rpta

@router.delete("/delete_monitor_materia/{id_materia}")
async def delete_monitor_materia(id_materia: int):
    rpta = nueva_monitor_materias.delete_monitor_materia(id_materia)
    return rpta