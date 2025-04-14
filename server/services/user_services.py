from fastapi import Request
from models.users import User
from password_validator import PasswordValidator
from utils.session_manager import SessionUser

from passlib.context import CryptContext

from fastapi.encoders import jsonable_encoder

schema = PasswordValidator()
_ = (
    schema.min(8)
    .max(20)
    .has()
    .uppercase()
    .has()
    .lowercase()
    .has()
    .digits()
    .has()
    .symbols()
    .has()
    .no()
    .spaces()
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(request: Request, userEmail: str) -> dict[str, str] | None:
    """Get user by email."""

    user: dict[str, str] | None = await request.app.mongodb["Users"].find_one(
        {"email": userEmail}
    )

    return user


async def user_login(request: Request, user: dict[str, str]) -> SessionUser | None:
    user_details: dict[str, str] | None = await request.app.mongodb["Users"].find_one(
        {"email": user["email"]}
    )

    if not user_details:
        return None

    session_user = SessionUser(
        user_details["email"],
        user_details["first_name"],
        user_details["last_name"],
        user_details["role"],
    )

    if (
        pwd_context.verify(user["password"], user_details["password"])
        and user_details["email"] == user["email"]
    ):
        return session_user

    return None


async def valid_new_email(request: Request, userEmail: str) -> bool:
    existing_user = await request.app.mongodb["Users"].find_one({"email": userEmail})

    return not bool(existing_user)


async def create_user(request: Request, user: User) -> bool:
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    user_JSON = jsonable_encoder(user)

    await request.app.mongodb["Users"].insert_one(user_JSON)

    new_user: dict[str, str] | None = await request.app.mongodb["Users"].find_one(
        {"email": user.email}
    )

    return bool(new_user)


async def update_user(user_id: int, user: User):
    pass


async def delete_user(user_id: int):
    pass
