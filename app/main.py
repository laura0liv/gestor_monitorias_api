from fastapi import FastAPI
from routes.monitoria_routes import router as monitoria_routes
from routes.seguimiento_academico_routes import router as seguimiento_academico_routes
from routes.sesion_seguimiento_routes import router as sesion_seguimiento_routes
from routes.horario_monitor_routes import router as horario_monitor_routes
from routes.estudiante_materia_routes import router as estudiante_materia_routes
from routes.materia_routes import router as materia_routes
from routes.rol_routes import router as rol_routes
from routes.usuario_routes import router as usuario_routes
from routes.aula_routes import router as aula_routes
from routes.programa_routes import router as programa_routes
from routes.calificacion_router import router as calificacion_routes
from routes.periodo_academico_routes import router as periodo_academico_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Sistema de Monitorías",
    description="API para la gestión de monitorías universitarias, estudiantes, materias y seguimiento académico.",
    version="1.0.0",
    docs_url="/docs",       # Swagger
    redoc_url="/redoc",     # Redoc
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # puerto de Svelte
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aula_routes)
app.include_router(calificacion_routes)
app.include_router(estudiante_materia_routes)
app.include_router(horario_monitor_routes)
app.include_router(materia_routes)
app.include_router(monitoria_routes)
app.include_router(periodo_academico_routes) 
app.include_router(programa_routes)
app.include_router(rol_routes)
app.include_router(seguimiento_academico_routes)
app.include_router(sesion_seguimiento_routes)
app.include_router(usuario_routes) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)