from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.aula_model import Aula
from controllers.aula_controller import AulaController

router = APIRouter(
    prefix="/aula",
    tags=["Aula"]
)
nuevo_aula = AulaController()


@router.get("/get_aulas/")
async def get_aulas():
    rpta = nuevo_aula.get_all_aula()
    return rpta
@router.get("/get_aula/{id_aula}")
async def get_aula(id_aula: int):
    rpta = nuevo_aula.get_aula(id_aula)
    return rpta 
@router.post("/create_aula/")
async def create_aula(aula: Aula):  
    aula_data = jsonable_encoder(aula)
    rpta = nuevo_aula.create_aula(aula_data)
    return rpta
@router.put("/update_aula/{id_aula}")       
async def update_aula(id_aula: int, aula: Aula):
    aula_data = jsonable_encoder(aula)
    rpta = nuevo_aula.update_aula(id_aula, aula_data)
    return rpta
@router.delete("/delete_aula/{id_aula}")
async def delete_aula(id_aula: int):
    rpta = nuevo_aula.delete_aula(id_aula)
    return rpta
