from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.programa_model import Programa
from controllers.programa_controller import ProgramaController

router = APIRouter()
nuevo_programa = ProgramaController()
@router.get("/get_programas/")
async def get_programas():
    rpta = nuevo_programa.get_all_programa()
    return rpta
@router.get("/get_programa/{id_programa}")
async def get_programa(id_programa: int):
    rpta = nuevo_programa.get_programa(id_programa)
    return rpta
@router.post("/create_programa/")
async def create_programa(programa: Programa):  
    programa_data = jsonable_encoder(programa)
    rpta = nuevo_programa.create_programa(programa_data)
    return rpta 
@router.put("/update_programa/{id_programa}")       
async def update_programa(id_programa: int, programa: Programa):
    programa_data = jsonable_encoder(programa)
    rpta = nuevo_programa.update_programa(id_programa, programa_data)
    return rpta
@router.delete("/delete_programa/{id_programa}")
async def delete_programa(id_programa: int):
    rpta = nuevo_programa.delete_programa(id_programa)
    return rpta