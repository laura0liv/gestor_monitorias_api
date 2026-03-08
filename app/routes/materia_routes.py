
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.materia_model import Materia
from controllers.materia_controller import MateriaController

router = APIRouter()
nueva_materia = MateriaController()

@router.get("/get_materia/")
async def get_materia():
    rpta = nueva_materia.get_all_materia()
    return rpta

@router.get("/get_materia/{id_materia}")
async def get_materia(id_materia: int): 
    rpta = nueva_materia.get_materia(id_materia)
    return rpta

@router.post("/create_materia/")
async def create_materia(materia: Materia): 
    materia_data = jsonable_encoder(materia)
    rpta = nueva_materia.create_materia(materia_data)
    return rpta

@router.put("/update_materia/{id_materia}")
async def update_materia(id_materia: int, materia: Materia):
    materia_data = jsonable_encoder(materia)
    rpta = nueva_materia.update_materia(id_materia, materia_data)
    return rpta

@router.delete("/delete_materia/{id_materia}")
async def delete_materia(id_materia: int):
    rpta = nueva_materia.delete_materia(id_materia)
    return rpta