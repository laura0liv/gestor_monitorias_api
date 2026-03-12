from fastapi import FastAPI
from routes.materia_routes import router as materia_routes
from routes.rol_routes import router as rol_routes
from routes.usuario_routes import router as usuario_routes
from routes.aula_routes import router as aula_routes
from routes.programa_routes import router as programa_routes
from routes.calificacion_router import router as calificacion_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    "https://ep-square-flower-aiq3n3y4-pooler.c-4.us-east-1.aws.neon.tech",
    "http://localhost"
    #"http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuario_routes)
app.include_router(aula_routes)
app.include_router(programa_routes)
app.include_router(calificacion_routes)
app.include_router(rol_routes)
app.include_router(materia_routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)