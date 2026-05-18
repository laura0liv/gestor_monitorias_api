from fastapi import APIRouter
from app.controllers.auth_controller import AuthController
from app.models.auth_model import LoginSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login(data: LoginSchema):
    return AuthController.login(data.dict())