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

# ✅ Sin barra final — coincide con el fetch del frontend
@router.post("/create_monitor_materia")
async def create_monitor_materia(monitor_materias: MonitorMateria):
    monitor_materia_data = jsonable_encoder(monitor_materias)
    return nueva_monitor_materias.create_monitor_materia(monitor_materia_data)

@router.put("/update_monitor_materia/{id_monitor}/{id_materia}")
async def update_monitor_materia(id_monitor: int, id_materia: int, monitor_materias: MonitorMateria):
    monitor_materia_data = jsonable_encoder(monitor_materias)
    return nueva_monitor_materias.update_monitor_materia(id_monitor, id_materia, monitor_materia_data)

# ✅ Query params en vez de path — coincide con el fetch del frontend
@router.delete("/delete_monitor_materia")
async def delete_monitor_materia(id_monitor: int, id_materia: int):
    return nueva_monitor_materias.delete_monitor_materia(id_monitor, id_materia)

@router.get("/get_monitors_and_subjects/")
async def get_monitors_and_subjects():
    return nueva_monitor_materias.get_monitors_and_subjects()

@router.delete("/delete_subject_from_monitor_if_admin/{current_user_role}/{id_monitor}/{id_materia}")
async def delete_subject_from_monitor_if_admin(current_user_role: int, id_monitor: int, id_materia: int):
    return nueva_monitor_materias.delete_subject_from_monitor_if_admin(current_user_role, id_monitor, id_materia)

@router.get("/get_materias_by_monitor/{id_monitor}")
async def get_materias_by_monitor(id_monitor: int):
    rpta = nueva_monitor_materias.get_materias_by_monitor(id_monitor)
    return rpta