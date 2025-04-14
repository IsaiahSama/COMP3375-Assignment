"""This will hold session related items"""

from fastapi import Request
from json import loads


class SessionUser:
    email: str
    firstname: str
    lastname: str
    role: str

    session_key: str = "user"

    def __init__(self, email: str, firstname: str, lastname: str, role: str):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role

    def set_session_user(self, request: Request):
        request.session[SessionUser.session_key] = self.to_json()

    def to_json(self) -> dict[str, str]:
        return {
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "role": self.role,
        }

    @staticmethod
    def from_json(data: dict[str, str] | str) -> "SessionUser":
        if isinstance(data, str):
            data: dict[str, str] = loads(data)

        return SessionUser(
            data["email"], data["firstname"], data["lastname"], data["role"]
        )

    @staticmethod
    def get_session_user(request: Request) -> "SessionUser | None":
        session_info: dict[str, str] | None = request.session.get(
            SessionUser.session_key, None
        )
        if not session_info:
            return None

        return SessionUser.from_json(session_info)
