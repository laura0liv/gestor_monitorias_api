from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from datetime import date, time

from app.controllers.monitoria_controller import MonitoriaController

router = APIRouter(prefix="/monitorias", tags=["Monitorías"])
controller = MonitoriaController()


# ──────────────────────────────────────────────────────
# SCHEMAS
# ──────────────────────────────────────────────────────

class SolicitarMonitoriaSchema(BaseModel):
    id_monitor: int
    id_estudiante: int
    id_materia: int
    id_aula: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    modalidad: str
    id_periodo: int
    observaciones: Optional[str] = None


class ResponderMonitoriaSchema(BaseModel):
    accion: str
    observaciones: Optional[str] = None


class AsistenciaSchema(BaseModel):
    asistencia: bool
    observaciones: Optional[str] = None


class UpdateMonitoriaSchema(BaseModel):
    id_monitor: int
    id_estudiante: int
    id_materia: int
    id_aula: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    modalidad: str
    estado: str
    id_periodo: int
    asistencia: Optional[bool] = None
    observaciones: Optional[str] = None


# ──────────────────────────────────────────────────────
# RUTAS GENERALES (admin)
# ──────────────────────────────────────────────────────

@router.get("/", summary="Listar todas las monitorías")
def get_all_monitorias():
    return controller.get_all_monitorias()


# ──────────────────────────────────────────────────────
# MÓDULO ESTUDIANTE — rutas estáticas primero
# ──────────────────────────────────────────────────────

@router.post(
    "/solicitar",
    summary="Solicitar monitoría (estudiante)",
    description=(
        "El estudiante solicita una monitoría con un tutor disponible. "
        "Valida disponibilidad del tutor y del estudiante antes de crear el registro."
    )
)
def solicitar_monitoria(body: SolicitarMonitoriaSchema):
    return controller.solicitar_monitoria(body.model_dump())


@router.get(
    "/disponibilidad/tutores",
    summary="Consultar tutores disponibles",
    description=(
        "Devuelve los tutores que pueden atender la materia solicitada "
        "en la fecha y bloque horario indicados, sin conflictos de agenda."
    )
)
def get_tutores_disponibles(
    id_materia:  int = Query(..., description="ID de la materia"),
    fecha:       str = Query(..., description="Fecha deseada (YYYY-MM-DD)"),
    hora_inicio: str = Query(..., description="Hora de inicio deseada (HH:MM)"),
    hora_fin:    str = Query(..., description="Hora de fin deseada (HH:MM)")
):
    return controller.get_tutores_disponibles(id_materia, fecha, hora_inicio, hora_fin)


@router.get(
    "/estudiante/{id_estudiante}",
    summary="Ver mis monitorías (estudiante)",
    description="Lista todas las monitorías del estudiante: pendientes, aceptadas, completadas, etc."
)
def get_monitorias_estudiante(id_estudiante: int):
    return controller.get_monitorias_estudiante(id_estudiante)


# ──────────────────────────────────────────────────────
# MÓDULO TUTOR — rutas estáticas primero
# ──────────────────────────────────────────────────────

@router.get(
    "/tutor/{id_monitor}",
    summary="Ver mis monitorías (tutor)",
    description="Lista todas las monitorías asignadas al tutor con información completa del estudiante."
)
def get_monitorias_tutor(id_monitor: int):
    return controller.get_monitorias_tutor(id_monitor)


@router.get(
    "/tutor/{id_monitor}/pendientes",
    summary="Ver solicitudes pendientes (tutor)",
    description="Lista las monitorías que el tutor aún no ha aceptado ni rechazado."
)
def get_monitorias_tutor_pendientes(id_monitor: int):
    return controller.get_monitorias_tutor_pendientes(id_monitor)


# ──────────────────────────────────────────────────────
# RUTAS DINÁMICAS — siempre al final
# ──────────────────────────────────────────────────────

@router.get("/{id_monitoria}", summary="Obtener detalle de una monitoría")
def get_monitoria(id_monitoria: int):
    return controller.get_monitoria(id_monitoria)


@router.put("/{id_monitoria}", summary="Actualizar monitoría (admin)")
def update_monitoria(id_monitoria: int, body: UpdateMonitoriaSchema):
    return controller.update_monitoria(id_monitoria, body.model_dump())


@router.delete("/{id_monitoria}", summary="Eliminar monitoría (soft delete)")
def delete_monitoria(id_monitoria: int):
    return controller.delete_monitoria(id_monitoria)


@router.patch(
    "/{id_monitoria}/cancelar/estudiante/{id_estudiante}",
    summary="Cancelar monitoría (estudiante)",
    description="El estudiante cancela una monitoría propia que aún esté en estado 'Pendiente'."
)
def cancelar_monitoria_estudiante(id_monitoria: int, id_estudiante: int):
    return controller.cancelar_monitoria_estudiante(id_monitoria, id_estudiante)


@router.patch(
    "/{id_monitoria}/responder/tutor/{id_monitor}",
    summary="Aceptar o rechazar monitoría (tutor)",
    description="El tutor acepta o rechaza una monitoría pendiente. Acción: 'Aceptada' | 'Rechazada'."
)
def responder_monitoria(id_monitoria: int, id_monitor: int, body: ResponderMonitoriaSchema):
    return controller.responder_monitoria(
        id_monitoria,
        id_monitor,
        body.accion,
        body.observaciones
    )


@router.patch(
    "/{id_monitoria}/asistencia/tutor/{id_monitor}",
    summary="Registrar asistencia (tutor)",
    description="El tutor marca si el estudiante asistió. Cambia el estado a 'Completada'."
)
def registrar_asistencia(id_monitoria: int, id_monitor: int, body: AsistenciaSchema):
    return controller.registrar_asistencia(
        id_monitoria,
        id_monitor,
        body.asistencia,
        body.observaciones
    )