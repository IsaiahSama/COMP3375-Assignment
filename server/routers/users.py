from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from models.users import User
from services import user_services
from utils.session_manager import SessionUser
from utils.helper import build_context

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["User"])


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("user/login.html", context={"request": request})


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "user/register.html", context={"request": request}
    )


@router.get("/profile")
async def profile_page(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login")
    logged_in_user = request.session.get("user")
    return templates.TemplateResponse(
        "user/profile.html", context={"request": request, "user": logged_in_user}
    )


@router.get("/logout")
async def logout_page(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login")
    if "user" in request.session:
        del request.session["user"]
    return RedirectResponse(url="/login", status_code=303)


# @router.post("/logout")
# async def logout(request: Request):
#     if "user" in request.session:
#         del request.session["user"]
#     return RedirectResponse(url="user/login", status_code=303)


class LoginForm(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(request: Request, body: Annotated[LoginForm, Form()]):
    user = {"email": body.email, "password": body.password}

    user_authenticated: SessionUser | None = await user_services.user_login(
        request, user
    )

    if user_authenticated:
        # Set session or token here
        request.session["user"] = user_authenticated
        return RedirectResponse("/")
    else:
        return templates.TemplateResponse(
            "user/login.html",
            context=build_context(request, {"error": "Invalid Credentials"}),
        )


class RegisterForm(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str


@router.post("/register")
async def register(request: Request, body: Annotated[RegisterForm, Form()]):
    user = User(
        first_name=body.firstname,
        last_name=body.lastname,
        email=body.email,
        password=body.password,
    )

    return_page = "user/register.html"

    email_exists = await user_services.email_exists(request, user.email)

    if email_exists:
        return templates.TemplateResponse(
            return_page,
            context=build_context(request, {"error": "This email is already taken"}),
        )

    error_info: dict[str, str] = await user_services.validate_new_info(user)

    if "error" in error_info and error_info["error"] != "":
        return templates.TemplateResponse(
            return_page,
            context=build_context(request, {"error": error_info["error"]}),
        )

    success = await user_services.create_user(request, user)

    if success:
        return RedirectResponse("/", 201)
    else:
        return templates.TemplateResponse(
            return_page,
            context=build_context(
                request, {"error": "Your account could not be created at this time"}
            ),
        )
