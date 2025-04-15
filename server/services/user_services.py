from fastapi import Request
from models.users import User
from password_validator import PasswordValidator
from .session_manager_service import SessionUser
from .db_collections import Collections

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

    user: dict[str, str] | None = await request.app.mongodb[
        Collections.USER.value
    ].find_one({"email": userEmail})

    return user


async def user_login(request: Request, user: dict[str, str]) -> SessionUser | None:
    user_details: dict[str, str] | None = await request.app.mongodb[
        Collections.USER.value
    ].find_one({"email": user["email"]})

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


async def email_exists(request: Request, userEmail: str) -> bool:
    existing_user = await request.app.mongodb[Collections.USER.value].find_one(
        {"email": userEmail}
    )

    return bool(existing_user)


async def validate_new_info(user: User) -> dict[str, str]:
    results = {"error": ""}

    user.first_name = user.first_name.strip()
    user.last_name = user.last_name and user.last_name.strip() or ""

    # Check First Name
    if not user.first_name.isalpha():
        results["error"] = "First name should only consist of letters."

    # Check Last Name
    if user.last_name and not user.last_name.isalpha():
        results["error"] = "Last name should only consist of letters."

    # Check Email
    if "@" not in user.email:
        results["error"] = "Expected an @ in the email"

    # Check Password Strength

    if len(user.password) < 8:
        results["error"] = "Password must be greater than 8 characters"

    return results


async def create_user(request: Request, user: User) -> bool:
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    user_JSON = jsonable_encoder(user)

    await request.app.mongodb[Collections.USER.value].insert_one(user_JSON)

    new_user: dict[str, str] | None = await request.app.mongodb[
        Collections.USER.value
    ].find_one({"email": user.email})

    return bool(new_user)


async def update_user(user_id: int, user: User):
    pass


async def delete_user(user_id: int):
    pass
