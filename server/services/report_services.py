from fastapi import Request
from server.models.pothole import Pothole


async def create_report(request: Request, report: Pothole) -> bool:
    """Create a new report."""
    success = True

    print("Pothole Received!")
    print(f"{report=}")

    return success


async def edit_report(request: Request, report: Pothole) -> bool:
    """Edit an existing report."""
    success = True
    return success


async def delete_report(request: Request, report: int) -> bool:
    """Delete a report."""
    success = True
    return success
