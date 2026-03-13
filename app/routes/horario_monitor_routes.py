from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.horario_monitor_model import HorarioMonitor
from controllers.horario_monitor_controller import HoriarioMonitorController

router = APIRouter(
    prefix="/horario_monitor",
    tags=["Horario Monitor"]
)
nuevo_horario_monitor = HoriarioMonitorController()


@router.get("/get_horario_monitors/")
async def get_horario_monitors():
    rpta = nuevo_horario_monitor.get_all_horario_monitors()
    return rpta

@router.get("/get_horario/{id_estudiante}")
async def get_horario(id_estudiante: int):
    rpta = nuevo_horario_monitor.get_horario(id_estudiante)
    return rpta 

@router.post("/create_horario_monitor/")
async def create_horario_monitor(horario_monitor: HorarioMonitor):  
    horario_monitor_data = jsonable_encoder(horario_monitor)
    rpta = nuevo_horario_monitor.create_horario_monitor(horario_monitor_data)
    return rpta

@router.put("/update_horario_monitor/{id_estudiante}")       
async def update_horario_monitor(id_estudiante: int, horario_monitor: HorarioMonitor):
    horario_monitor_data = jsonable_encoder(horario_monitor)
    rpta = nuevo_horario_monitor.update_horario_monitor(id_estudiante, horario_monitor_data)
    return rpta

@router.delete("/delete_horario_monitor/{id_estudiante}")
async def delete_horario_monitor(id_estudiante: int):
    rpta = nuevo_horario_monitor.delete_horario_monitor(id_estudiante)
    return rpta
