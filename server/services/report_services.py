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
    dumped_model["display_id"] = dumped_model["id"][:5]

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

    return reports


async def get_reports_by_email(request: Request) -> list[dict[str, str]]:
    user_email = request.session.get("user", {}).get("email", None)

    if not user_email:
        return []

    user_reports = (
        await request.app.mongodb[Collections.REPORT.value]
        .find({"user_email": user_email})
        .to_list()
    )

    return user_reports


async def get_report_by_id(request: Request, report_id: str) -> dict[str, str] | None:
    return request.app.mongodb[Collections.REPORT.value].find_one({"id": report_id})
