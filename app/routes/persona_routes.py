from fastapi import APIRouter, HTTPException
from controllers.persona_controller import *
from models.persona_model import Persona

router = APIRouter()

nueva_persona = PersonaController()


@router.post("/create_persona")
async def create_persona(user: Persona):
    rpta = nueva_persona.create_persona(user)
    return rpta


@router.get("/get_persona/{persona_id}",response_model=Persona)
async def get_persona(persona_id: int):
    rpta = nueva_persona.get_persona(persona_id)
    return rpta

@router.get("/get_personas/")
async def get_personas():
    rpta = nueva_persona.get_personas()
    return rpta

@router.put("/update_persona/{id_persona}")
async def update_persona(id_persona: int, persona: Persona):
    rpta = nueva_persona.update_persona(id_persona, persona)
    return rpta

@router.delete("/delete_persona/{id_persona}", response_model=Persona)
async def delete_persona(id_persona: int):
    return nueva_persona.delete_persona(id_persona)