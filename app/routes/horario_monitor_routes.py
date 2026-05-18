from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.models.horario_monitor_model import HorarioMonitor
from app.controllers.horario_monitor_controller import HorarioMonitorController

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
    return nuevo_horario_monitor.get_horario_monitor(id_horario)


@router.post("/create_horario_monitor/")
async def create_horario_monitor(horario_monitor: HorarioMonitor):
    horario_monitor_data = jsonable_encoder(horario_monitor)
    return nuevo_horario_monitor.create_horario_monitor(horario_monitor_data)


@router.put("/update_horario_monitor/{id_horario}")
async def update_horario_monitor(id_horario: int, horario_monitor: HorarioMonitor):
    horario_monitor_data = jsonable_encoder(horario_monitor)
    return nuevo_horario_monitor.update_horario_monitor(id_horario, horario_monitor_data)


@router.delete("/delete_horario_monitor/{id_horario}")
async def delete_horario_monitor(id_horario: int):
    return nuevo_horario_monitor.delete_horario_monitor(id_horario)


@router.get("/get_horarios_monitor/{id_monitor}")
async def get_horarios_by_monitor(id_monitor: int):
    return nuevo_horario_monitor.get_horarios_by_monitor(id_monitor)


@router.delete("/delete_horarios_monitor/{id_monitor}")
async def delete_horarios_by_monitor(id_monitor: int):
    return nuevo_horario_monitor.delete_horarios_by_monitor(id_monitor)


# ─────────────────────────────────────────────────────────────
# NUEVO — consumido por SolicitarMonitoria.svelte paso 3
#
# El frontend llama: GET /disponibilidad/get_disponibilidad/{id}
# Se registra como segundo router en main.py con prefix="/disponibilidad"
# ─────────────────────────────────────────────────────────────

disponibilidad_router = APIRouter(
    prefix="/disponibilidad",
    tags=["Disponibilidad"]
)

@disponibilidad_router.get(
    "/get_disponibilidad/{id_monitor}",
    summary="Slots libres del monitor para la próxima semana",
    description="""
    Consumido por SolicitarMonitoria.svelte en el paso 3.

    Retorna los bloques de horario del monitor que NO tienen una monitoría
    activa (Pendiente o Programada) en la próxima ocurrencia de ese día.

    Campos: dia_semana, hora_inicio "HH:MM", hora_fin "HH:MM"
    """
)
async def get_disponibilidad_monitor(id_monitor: int):
    return nuevo_horario_monitor.get_disponibilidad_monitor(id_monitor)