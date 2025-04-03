from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from server.models.users import User

templates = Jinja2Templates(directory="templates/user")
router = APIRouter(prefix="/user", tags=["User"])

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", context={"request": request})

@router.get("/profile")
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", context={"request": request})

@router.get("/logout")
async def logout_page(request: Request):
    return templates.TemplateResponse("logout.html", context={"request": request})

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