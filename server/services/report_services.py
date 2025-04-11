from typing import List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from server.models.pothole import Pothole


async def create_report(request: Request, report: Pothole) -> bool:
    """Create a new report."""
    success = True

    dumped_model = jsonable_encoder(report)
    del dumped_model["id"]

    user_email = request.session.get("user", {}).get(
        "email", None
    )  # get_user_email_from_session()

    dumped_model["user_email"] = user_email

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


async def get_all_reports(request: Request) -> List[Pothole]:
    reports = await request.app.mongodb["Pothole"].find().to_list()

    return reports


async def get_reports(request: Request) -> List[Pothole]:
    user_email = request.session.get("user", {}).get("email", None)

    reports = await request.app.mongodb["Pothole"].find({"email": user_email}).to_list()
    
    user_reports = [report for report in reports if report["user_email"] == user_email]

    return user_reports
