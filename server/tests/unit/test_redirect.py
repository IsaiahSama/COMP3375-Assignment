from fastapi.testclient import TestClient
from enum import Enum
from bs4 import BeautifulSoup

from server import app

client = TestClient(app)


class Routes(Enum):
    HOME = "/"
    LOGIN = "/login"
    PROFILE = "/profile"
    REPORT_CREATE = "/reports/create"
    REPORT_VIEW = "/reports"


def test_unauthorized_redirect():
    routes = [
        Routes.HOME.value,
        Routes.PROFILE.value,
        Routes.REPORT_CREATE.value,
        Routes.REPORT_VIEW.value,
    ]

    for route in routes:
        response = client.get(route)

        assert response.status_code == 200

        soup = BeautifulSoup(response.text, "html.parser")
        assert soup.title is not None and soup.title.string is not None

        assert "Login" in soup.title.string
