from fastapi import Request
from server.models.users import User
from password_validator import PasswordValidator

from passlib.context import CryptContext

from fastapi.encoders import jsonable_encoder

schema = PasswordValidator()
schema.min(8).max(
    20
).has().uppercase().has().lowercase().has().digits().has().symbols().has().no().spaces()

user_validation = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(regUser):
    """Get user by email."""
    user = await regUser.app.mongodb["Users"].find_one({"email": regUser.email})
    if user:
        return user
    else:
        return None

async def user_login(user, request: Request):
    user_check = await request.app.mongodb["Users"].find_one({"email": user["email"]})
    if user_check:
        user_return = {
            "email": user_check["email"],
            "first_name": user_check["first_name"],
            "last_name": user_check["last_name"],
            "role": user_check["role"]
        }
        if pwd_context.verify(user["password"], user_check["password"])  and user_check["email"] == user["email"]:
            return user_return
        else:
            return None
    else:
        return None


async def create_user(user: User, request: Request):
    user_JSON = jsonable_encoder(user)

    exisiting_user = await request.app.mongodb["Users"].find_one({"email": user.email})
    if exisiting_user:
        user_validation["valid_email"] = False
    else:
        user_validation["valid_email"] = True

    if not schema.validate(user.password):
        user_validation["valid_pass"] = False
    else:
        user_validation["valid_pass"] = True

    if not user_validation.get("valid_pass", True) or not user_validation.get(
        "valid_email", True
    ):
        return user_validation

    else:
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password
        user_JSON = jsonable_encoder(user)
        await request.app.mongodb["Users"].insert_one(user_JSON)
        new_user = await request.app.mongodb["Users"].find_one({"email": user.email})
        print(new_user)
        return user_validation


async def update_user(user_id: int, user: User):
    pass


async def delete_user(user_id: int):
    pass
