from fastapi import Request
from fastapi.encoders import jsonable_encoder
from models.report import Report
from .db_collections import Collections


async def create_report(request: Request, report: Report) -> bool:
    """Create a new report."""
    success = True

    dumped_model = jsonable_encoder(report)

    user_email = request.session.get("user", {}).get(
        "email", None
    )  # get_user_email_from_session()

    dumped_model["user_email"] = user_email

    await request.app.mongodb[Collections.REPORT.value].insert_one(dumped_model)

    return success


async def edit_report(request: Request, report: Report) -> bool:
    """Edit an existing report."""
    success = True

    return success


async def delete_report(request: Request, report: int) -> bool:
    """Delete a report."""
    success = True
    return success


async def get_all_reports(request: Request) -> list[dict[str, str]]:
    reports: list[dict[str, str]] = (
        await request.app.mongodb[Collections.REPORT.value].find().to_list()
    )

    for report in reports:
        report["display_id"] = report["id"][:5]

    return reports


async def get_reports(request: Request) -> list[dict[str, str]]:
    user_email = request.session.get("user", {}).get("email", None)

    if not user_email:
        return []

    reports = await get_all_reports(request)

    user_reports = [report for report in reports if report["user_email"] == user_email]

    return user_reports
