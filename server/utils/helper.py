"""Helper functions can go here!"""

from fastapi import Request
from typing import Any


def build_context(request: Request, items: dict[str, Any]) -> dict[str, Any]:
    context = {"request": request}

    context.update(items)
    return context
