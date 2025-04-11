from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from server.models.users import User
from server.services.user_services import create_user, user_login

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["User"])

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("user/login.html", context={"request": request})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("user/register.html", context={"request": request})

@router.get("/profile")
async def profile_page(request: Request):
    logged_in_user = request.session.get("user")
    return templates.TemplateResponse("user/profile.html", context={"request": request, "user": logged_in_user})

@router.get("/logout")
async def logout_page(request: Request):
    return templates.TemplateResponse("logout.html", context={"request": request})

class LoginForm(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: Request, body: Annotated[LoginForm, Form()]):
    user = {
        "email": body.email,
        "password": body.password
    }
    user_authenticated = await user_login(user, request)  # Assuming user_login is a function that checks the user's credentials
    if user_authenticated:
        if "user" in request.session:
            del request.session["user"]  # Remove existing session if any
        # Set session or token here
        request.session["user"] = user_authenticated
        return RedirectResponse(url="/", status_code=303)
    # Ensure the passwords match
    else:
        return templates.TemplateResponse("user/register.html", context={"request": request, "error": "Invalid Credentials"})


class RegisterForm(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

@router.post("/register")
async def register(request: Request, body: Annotated[RegisterForm, Form()]):
    print("in regiser post route")

    user = User(first_name=body.firstname, last_name=body.lastname, email=body.email, password=body.password)
    user_create =await create_user(user, request)
    if user_create["valid_pass"] and user_create["valid_email"]:
        print(user_create)
        return RedirectResponse(url="/", status_code=303)
    
    else:
        if not user_create["valid_email"] and not user_create["valid_pass"]:
            # Handle both invalid password and email error
            return templates.TemplateResponse("user/register.html", context={"request": request, "error": "Invalid email and password"})
        if not user_create["valid_pass"]:
            # Handle invalid password error
            return templates.TemplateResponse("user/register.html", context={"request": request, "error": "Invalid password"})
        if not user_create["valid_email"]:
            # Handle invalid email error
            return templates.TemplateResponse("user/register.html", context={"request": request, "error": "Invalid email"})
        
    
