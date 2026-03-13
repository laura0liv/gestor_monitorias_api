from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.estudiante_materia_model import EstudianteMateria
from controllers.estudiante_materia_controller import EstudianteMateriaController

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
