from typing import Annotated
from fastapi import APIRouter, Request, Form
from pydantic import BaseModel
from server.models.users import User

router = APIRouter(prefix="/users", tags=["Users"])

class LoginForm(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: Request, body: Annotated[LoginForm, Form()]):
    user = None # Find user via email
    # Ensure the passwords match
    
    return user

class RegisterForm(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

@router.post("/register")
async def register(request: Request, body: Annotated[RegisterForm, Form()]):
    user = User(first_name=body.firstname, last_name=body.lastname, email=body.email, password=body.password)
    return user