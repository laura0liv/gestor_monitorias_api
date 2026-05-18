from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.models.estudiante_materia_model import EstudianteMateria
from app.controllers.estudiante_materia_controller import EstudianteMateriaController

router = APIRouter(
    prefix="/estudiante_materia",
    tags=["Estudiante Materia"]
)
nuevo_estudiante_materia = EstudianteMateriaController()


@router.get("/get_estudiante_materias/")
async def get_estudiante_materias():
    rpta = nuevo_estudiante_materia.get_all_estudiante_materias()
    return rpta


@router.get("/get_estudiante_materia/{id_estudiante}")
async def get_estudiante_materia(id_estudiante: int):
    rpta = nuevo_estudiante_materia.get_estudiante_materia(id_estudiante)
    return rpta


@router.post("/create_estudiante_materia/")
async def create_estudiante_materia(estudiante_materia: EstudianteMateria):
    estudiante_materia_data = jsonable_encoder(estudiante_materia)
    rpta = nuevo_estudiante_materia.create_estudiante_materia(estudiante_materia_data)
    return rpta


@router.put("/update_estudiante_materia/{id_estudiante}")
async def update_estudiante_materia(id_estudiante: int, estudiante_materia: EstudianteMateria):
    estudiante_materia_data = jsonable_encoder(estudiante_materia)
    rpta = nuevo_estudiante_materia.update_estudiante_materia(id_estudiante, estudiante_materia_data)
    return rpta


@router.delete("/delete_estudiante_materia/{id_estudiante}")
async def delete_estudiante_materia(id_estudiante: int):
    rpta = nuevo_estudiante_materia.delete_estudiante_materia(id_estudiante)
    return rpta


# ─────────────────────────────────────────────────────────────
# NUEVO — materias del estudiante en el período activo
# Retorna los mismos campos que /materia/disponibles
# para reutilizar MateriasEstudiante.svelte filtrando por alumno
# ─────────────────────────────────────────────────────────────

@router.get(
    "/materias/{id_estudiante}",
    summary="Materias inscritas por el estudiante en el período activo",
    description="""
    Retorna las materias del período académico activo en las que
    el estudiante está matriculado, con conteo de monitores disponibles.

    Mismos campos que GET /materia/disponibles:
      - id_materia, nombre_materia, creditos,
        nombre_programa, monitores_disponibles
    """
)
async def get_materias_por_estudiante(id_estudiante: int):
    rpta = nuevo_estudiante_materia.get_materias_por_estudiante(id_estudiante)
    return rpta