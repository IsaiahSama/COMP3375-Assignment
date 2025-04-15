import pytest
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from services.user_services import get_user, validate_new_info
from utils.config import config

# Let's Fake some Stuff!


class App:
    """This is a fake app that just has a mongodb client"""

    client: AsyncIOMotorClient
    mongodb: AsyncIOMotorDatabase

    def __init__(self):
        self.client = AsyncIOMotorClient(
            config.mongo_uri
        )  # This is indeed the real client 🤣🤣

        self.mongodb = self.client.get_database(config.mongo_db_name)


class Request:
    """This is a fake request object, that provides access to a monogo client through request.app.mongodb"""

    app: App

    def __init__(self, app: App):
        self.app = app


# Now we can do the tests we want


@pytest.mark.asyncio
async def test_get_user_by_email():
    request = Request(App())
    cases = [("notFound@mail.com", False), ("user@mail.com", True)]

    for case in cases:
        print(f"{case=}")
        result = await get_user(request, case[0])
        assert bool(result) == case[1]


@pytest.mark.asyncio
async def test_user_info_valid():
    class User:
        first_name: str
        last_name: str
        email: str
        password: str
        error: str

        def __init__(
            self, fname: str, lname: str, email: str, password: str, error: str
        ):
            self.first_name = fname
            self.last_name = lname
            self.email = email
            self.password = password
            self.error = error

    users = [
        User(
            "Invalid1",
            "Name",
            "valid@mail.com",
            "longerPassword",
            "First name should only consist of letters.",
        ),
        User("Test", "User", "test@mail.com", "securePassword", ""),
        User(
            "Valid",
            "Name",
            "invalidmail.com",
            "veryLongPassword",
            "Expected an @ in the email",
        ),
        User(
            "name",
            "one",
            "secure@mail.c",
            "pass",
            "Password must be longer than 8 characters",
        ),
    ]

    for user in users:
        result = await validate_new_info(user)
        assert result["error"] == user.error
