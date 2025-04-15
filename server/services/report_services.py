from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from models.enums import Severity, Status
from models.report import Report
from services.user_services import get_user
from .db_collections import Collections


class ReportTemplate(BaseModel):
    id: str
    location: str
    description: str
    severity: Severity
    status: Status


async def get_report_stats(request: Request) -> dict[str, str | int]:
    stats = {
        "Total Reports": 0,
        "In Progress": 0,
        "Completed": 0,
        "Biggest Contributor": "",
    }

    reports = await get_all_reports(request)

    stats["Total Reports"] = len(reports)
    stats["In Progress"] = len(
        [report for report in reports if report["status"] == Status.IN_PROGRESS.value]
    )
    stats["Completed"] = len(
        [report for report in reports if report["status"] == Status.COMPLETE.value]
    )

    contributors: dict[str, int] = {}

    for report in reports:
        contributors.setdefault(report["user_email"], 0)
        contributors[report["user_email"]] += 1

    biggest_contributor = "???"

    if contributors:
        biggest_contributor_email = max(contributors, key=lambda x: contributors[x])
        user = await get_user(request, biggest_contributor_email)
        if user:
            biggest_contributor = user["first_name"]

    stats["Biggest Contributor"] = biggest_contributor

    return stats


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


async def edit_report(request: Request, report: ReportTemplate) -> bool:
    """Edit an existing report."""
    success = True

    # Determine later if this person has permission to edit this resource.

    to_update = {
        "location": report.location,
        "description": report.description,
        "severity": report.severity.value,
        "status": report.status.value,
    }

    await request.app.mongodb[Collections.REPORT.value].update_one(
        {"id": report.id}, {"$set": to_update}
    )

    return success


async def delete_report(request: Request, report_id: str) -> bool:
    """Delete a report."""
    success = True

    # Again... Ideally, you'd want to perform some auth checks
    # Only people that should be able to modify a report is an admin and the original poster.

    await request.app.mongodb[Collections.REPORT.value].delete_one({"id": report_id})

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
    return await request.app.mongodb[Collections.REPORT.value].find_one(
        {"id": report_id}
    )
