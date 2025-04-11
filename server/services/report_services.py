from fastapi import Request
from fastapi.encoders import jsonable_encoder
from server.models.pothole import Pothole


async def create_report(request: Request, report: Pothole) -> bool:
    """Create a new report."""
    success = True

    dumped_model = jsonable_encoder(report)
    del dumped_model["id"]
    await request.app.mongodb["Pothole"].insert_one(dumped_model)

    return success


async def edit_report(request: Request, report: Pothole) -> bool:
    """Edit an existing report."""
    success = True
    return success


async def delete_report(request: Request, report: int) -> bool:
    """Delete a report."""
    success = True
    return success
