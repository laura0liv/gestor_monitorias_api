from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.monitoria_routes import router as monitoria_routes
from app.routes.monitor_materia_routes import router as monitor_materia_routes
from app.routes.seguimiento_academico_routes import router as seguimiento_academico_routes
from app.routes.sesion_seguimiento_routes import router as sesion_seguimiento_routes
from app.routes.horario_monitor_routes import (
    router as horario_monitor_routes,
    disponibilidad_router
)
from app.routes.estudiante_materia_routes import router as estudiante_materia_routes
from app.routes.materia_routes import router as materia_routes
from app.routes.rol_routes import router as rol_routes
from app.routes.usuario_routes import router as usuario_routes
from app.routes.aula_routes import router as aula_routes
from app.routes.programa_routes import router as programa_routes
from app.routes.calificacion_router import router as calificacion_routes
from app.routes.periodo_academico_routes import router as periodo_academico_routes
from app.routes.monitor_materia_routes import (
    router as monitor_materia_router,
    monitores_router
)

from app.routes.auth_routes import router as auth_router


app = FastAPI(
    title="API Sistema de Monitorías",
    description="API para la gestión de monitorías universitarias, estudiantes, materias y seguimiento académico.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(aula_routes)
app.include_router(monitor_materia_routes)
app.include_router(calificacion_routes)
app.include_router(estudiante_materia_routes)
app.include_router(horario_monitor_routes)
app.include_router(disponibilidad_router)
app.include_router(materia_routes)
app.include_router(monitoria_routes)
app.include_router(periodo_academico_routes)
app.include_router(programa_routes)
app.include_router(rol_routes)
app.include_router(seguimiento_academico_routes)
app.include_router(sesion_seguimiento_routes)
app.include_router(usuario_routes)
app.include_router(monitor_materia_router)
app.include_router(monitores_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)