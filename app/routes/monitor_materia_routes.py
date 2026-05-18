from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.controllers.monitor_materia_controller import MonitorMateriaController
from app.models.monitor_materia_model import MonitorMateria

router = APIRouter(
    prefix="/monitor_materia",
    tags=["Monitor Materia"]
)
nueva_monitor_materias = MonitorMateriaController()


@router.get("/get_monitor_materias/")
async def get_monitor_materias():
    return nueva_monitor_materias.get_all_monitor_materias()


@router.get("/get_monitor_materia/{id_monitor}/{id_materia}")
async def get_monitor_materia(id_monitor: int, id_materia: int):
    return nueva_monitor_materias.get_monitor_materia(id_monitor, id_materia)


@router.post("/create_monitor_materia")
async def create_monitor_materia(monitor_materias: MonitorMateria):
    monitor_materia_data = jsonable_encoder(monitor_materias)
    return nueva_monitor_materias.create_monitor_materia(monitor_materia_data)


@router.put("/update_monitor_materia/{id_monitor}/{id_materia}")
async def update_monitor_materia(id_monitor: int, id_materia: int, monitor_materias: MonitorMateria):
    monitor_materia_data = jsonable_encoder(monitor_materias)
    return nueva_monitor_materias.update_monitor_materia(id_monitor, id_materia, monitor_materia_data)


@router.delete("/delete_monitor_materia")
async def delete_monitor_materia(id_monitor: int, id_materia: int):
    return nueva_monitor_materias.delete_monitor_materia(id_monitor, id_materia)


@router.get("/get_monitors_and_subjects/")
async def get_monitors_and_subjects():
    return nueva_monitor_materias.get_monitors_and_subjects()


@router.get("/get_materias_by_monitor/{id_monitor}")
async def get_materias_by_monitor(id_monitor: int):
    return nueva_monitor_materias.get_materias_by_monitor(id_monitor)


# ─────────────────────────────────────────────────────────────
# NUEVO — consumido por SolicitarMonitoria.svelte paso 2
#
# El frontend llama: GET /monitores/por_materia/{id_materia}
# IMPORTANTE: en main.py registra este router también con
# prefix="/monitores" o agrega la ruta aquí con path completo.
# La solución más limpia es agregar un segundo router en este
# mismo archivo con prefix="/monitores".
# ─────────────────────────────────────────────────────────────

monitores_router = APIRouter(
    prefix="/monitores",
    tags=["Monitores"]
)

@monitores_router.get(
    "/por_materia/{id_materia}",
    summary="Monitores disponibles para una materia",
    description="""
    Consumido por SolicitarMonitoria.svelte en el paso 2.

    Retorna los monitores activos asignados a la materia indicada
    con su calificación promedio (de monitorías completadas).

    Campos: id_usuario, nombre, apellido, promedio_calificacion
    """
)
async def get_monitores_por_materia(id_materia: int):
    return nueva_monitor_materias.get_monitores_por_materia(id_materia)