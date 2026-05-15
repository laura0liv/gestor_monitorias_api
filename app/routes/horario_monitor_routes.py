from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from models.horario_monitor_model import HorarioMonitor
from controllers.horario_monitor_controller import HorarioMonitorController

router = APIRouter(
    prefix="/horario_monitor",
    tags=["Horario Monitor"]
)

nuevo_horario_monitor = HorarioMonitorController()


@router.get("/get_horario_monitors/")
async def get_horario_monitors():
    return nuevo_horario_monitor.get_all_horario_monitors()


@router.get("/get_horario/{id_horario}")
async def get_horario(id_horario: int):
    return nuevo_horario_monitor.get_horario(id_horario)


@router.post("/create_horario_monitor/")
async def create_horario_monitor(horario_monitor: HorarioMonitor):
    horario_monitor_data = jsonable_encoder(horario_monitor)
    return nuevo_horario_monitor.create_horario_monitor(horario_monitor_data)


@router.put("/update_horario_monitor/{id_horario}")
async def update_horario_monitor(id_horario: int, horario_monitor: HorarioMonitor):
    horario_monitor_data = jsonable_encoder(horario_monitor)
    return nuevo_horario_monitor.update_horario_monitor(
        id_horario,
        horario_monitor_data
    )


@router.delete("/delete_horario_monitor/{id_horario}")
async def delete_horario_monitor(id_horario: int):
    return nuevo_horario_monitor.delete_horario_monitor(id_horario)


@router.get("/get_horarios_monitor/{id_monitor}")
async def get_horarios_by_monitor(id_monitor: int):
    return nuevo_horario_monitor.get_horarios_by_monitor(id_monitor)


@router.delete("/delete_horarios_monitor/{id_monitor}")
async def delete_horarios_by_monitor(id_monitor: int):
    return nuevo_horario_monitor.delete_horarios_by_monitor(id_monitor)