from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from services import report_services
from services.report_services import ReportTemplate
from services.session_manager_service import SessionUser
from utils.helper import build_context
from models.report import Report
from typing import Annotated
from pydantic import BaseModel
from models.enums import Severity, Status

import uuid

router = APIRouter(prefix="/reports", tags=["Reports"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def reports_page(request: Request):
    user = SessionUser.get_session_user(request)
    if not user:
        return RedirectResponse("/login", 302)

    if user.role != "admin":
        reports = await report_services.get_reports_by_email(request)
    else:
        reports = await report_services.get_all_reports(request)

    for report in reports:
        report["image_path"] = report["image_path"].lstrip("./")

    return templates.TemplateResponse(
        "reports/reports.html", context={"request": request, "reports": reports}
    )


@router.get("/create")
async def create_report_page(request: Request):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)
    return templates.TemplateResponse(
        "reports/create.html", context={"request": request}
    )


@router.get("/edit/{report_id}")
async def edit_report_page(request: Request, report_id: str):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)

    report = await report_services.get_report_by_id(request, report_id)

    if not report:
        return templates.TemplateResponse(
            "reports/edit.html",
            context=build_context(request, {"error": "This report could not be found"}),
            status_code=404,
        )

    return templates.TemplateResponse(
        "reports/edit.html", context=build_context(request, {"report": report})
    )


@router.get("/delete/{report_id}")
async def delete_report_page(request: Request, report_id: str):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)

    report = await report_services.get_report_by_id(request, report_id)
    if not report:
        return templates.TemplateResponse(
            "reports/delete.html",
            context=build_context(request, {"error": "This report could not be found"}),
            status_code=404,
        )

    return templates.TemplateResponse(
        "reports/delete.html", context={"request": request, "report": report}
    )


class ReportCreateForm(BaseModel):
    """Form for creating a new report."""

    location: str
    imgpath: str
    desc: str
    severity: Severity


@router.post("/create")
async def create_report_endpoint(
    request: Request, body: Annotated[ReportCreateForm, Form()]
):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)

    report = Report(
        location=body.location,
        image_path=body.imgpath,
        description=body.desc,
        severity=body.severity,
    )

    success = await report_services.create_report(request, report)

    if not success:
        pass  # Add some logic in here later

    return HTMLResponse(content=f"Report {report} created!", status_code=201)


class ReportEditForm(ReportTemplate):
    id: str
    location: str
    description: str
    severity: Severity
    status: Status


@router.post("/edit")
async def edit_report_endpoint(
    request: Request, report: Annotated[ReportEditForm, Form()]
):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)

    result = await report_services.edit_report(request, report)

    if not result:
        return templates.TemplateResponse(
            "report/edit.html",
            context=build_context(request, {"error": "Could not perform operation"}),
            status_code=400,
        )

    return RedirectResponse("/reports", 302)


@router.post("/delete/{report_id}")
async def delete_report_endpoint(request: Request, report_id: str):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)

    result = await report_services.delete_report(request, report_id)

    if not result:
        return templates.TemplateResponse(
            "report/reports.html",
            context=build_context(request, {"error": "Could not perform operation"}),
            status_code=400,
        )

    return RedirectResponse("/reports", 302)


@router.post("/image-upload")
async def report_image_upload(request: Request, image: UploadFile = File(...)):
    """This is the route to access the image upload form."""
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login", 302)

    path = ""
    filename = ""
    if image.file and image.filename:
        filename = "temp_" + str(uuid.uuid4()) + "." + image.filename.split(".")[-1]
        path = "./public/uploaded-images/" + filename

        with open(path, "wb") as fp:
            _ = fp.write(await image.read())

    if path == "":
        return RedirectResponse(
            "/", 302
        )  # This should return an error code for Missing fields

    return templates.TemplateResponse(
        "components/location_upload.html",
        context={"request": request, "img_path": filename},
    )


@router.get("/{report_id}")
async def view_report_page(request: Request, report_id: str):
    if not (user := SessionUser.get_session_user(request)):
        return RedirectResponse("/login", 302)

    reports = await report_services.get_reports_by_email(request)

    exists = True

    if not reports:
        exists = False

    selected_report = [report for report in reports if report_id == report["id"]]

    if not selected_report:
        exists = False

    if not exists:
        return templates.TemplateResponse(
            "reports/report.html",
            context=build_context(request, {"error": "Report could not be found"}),
            status_code=404,
        )

    report = selected_report[0]

    return templates.TemplateResponse(
        "reports/report.html", context=build_context(request, {"report": report})
    )
