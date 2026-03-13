from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from controllers.periodo_academico_controller import PeriodoAcademicoController
from models.periodo_academico_model import PeriodoAcademico

router = APIRouter(
    prefix="/periodo_academico",
    tags=["Periodo Academico"]
)
nuevo_periodo_academico = PeriodoAcademicoController()

@router.get("/get_periodos_academicos/")
async def get_periodos_academicos():
    rpta = nuevo_periodo_academico.get_all_periodo_academico()
    return rpta

@router.get("/get_periodo_academico/{id_periodo_academico}")
async def get_periodo_academico(id_periodo_academico: int):
    rpta = nuevo_periodo_academico.get_periodo_academico(id_periodo_academico)
    return rpta

@router.post("/create_periodo_academico/")
async def create_periodo_academico(periodo_academico: PeriodoAcademico):
    periodo_academico_data = jsonable_encoder(periodo_academico)
    rpta = nuevo_periodo_academico.create_periodo_academico(periodo_academico_data)
    return rpta

@router.put("/update_periodo_academico/{id_periodo_academico}")
async def update_periodo_academico(id_periodo_academico: int, periodo_academico: PeriodoAcademico):
    periodo_academico_data = jsonable_encoder(periodo_academico)
    rpta = nuevo_periodo_academico.update_periodo_academico(id_periodo_academico, periodo_academico_data)
    return rpta

@router.delete("/delete_periodo_academico/{id_periodo_academico}")
async def delete_periodo_academico(id_periodo_academico: int):
    rpta = nuevo_periodo_academico.delete_periodo_academico(id_periodo_academico)
    return rpta