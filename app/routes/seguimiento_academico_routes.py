
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.seguimiento_academico_model import SeguimientoAcademico
from controllers.seguimiento_academico_controller import SeguimientoAcademicoController

router = APIRouter(
    prefix="/seguimiento_academico",
    tags=["Seguimiento Academico"]
)
nuevo_seguimiento_academico = SeguimientoAcademicoController()

@router.get("/get_all_seguimiento_academico/")
async def get_all_seguimiento_academico():
    rpta = nuevo_seguimiento_academico.get_all_seguimiento_academico()
    return rpta

@router.get("/get_seguimiento_academico/{id_seguimiento_academico}")
async def get_seguimiento_academico(id_seguimiento_academico: int): 
    rpta = nuevo_seguimiento_academico.get_seguimiento_academico(id_seguimiento_academico)
    return rpta

@router.post("/create_seguimiento_academico/")
async def create_seguimiento_academico(seguimiento_academico: SeguimientoAcademico): 
    seguimiento_academico_data = jsonable_encoder(seguimiento_academico)
    rpta = nuevo_seguimiento_academico.create_seguimiento_academico(seguimiento_academico_data)
    return rpta

@router.put("/update_seguimiento_academico/{id_seguimiento_academico}")
async def update_seguimiento_academico(id_seguimiento_academico: int, seguimiento_academico: SeguimientoAcademico):
    seguimiento_academico_data = jsonable_encoder(seguimiento_academico)
    rpta = nuevo_seguimiento_academico.update_seguimiento_academico(id_seguimiento_academico, seguimiento_academico_data)
    return rpta

@router.delete("/delete_seguimiento_academico/{id_seguimiento_academico}")
async def delete_seguimiento_academico(id_seguimiento_academico: int):
    rpta = nuevo_seguimiento_academico.delete_seguimiento_academico(id_seguimiento_academico)
    return rpta