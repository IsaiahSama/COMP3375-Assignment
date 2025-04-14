from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from services.report_services import (
    create_report,
    edit_report,
    delete_report,
    get_all_reports,
    get_reports,
)
from utils.session_manager import SessionUser
from models.pothole import Pothole
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
        return RedirectResponse("/login")

    if user.role != "admin":
        reports = await get_reports(request)
    else:
        reports = await get_all_reports(request)

    for report in reports:
        report["image_path"] = report["image_path"].lstrip("./")

    return templates.TemplateResponse(
        "reports/report.html", context={"request": request, "reports": reports}
    )


@router.get("/edit")
async def edit_report_page(request: Request):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("reports/edit.html", context={"request": request})


@router.get("/create")
async def create_report_page(request: Request):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse(
        "reports/create.html", context={"request": request}
    )


@router.get("/delete")
async def delete_report_page(request: Request):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse(
        "reports/delete.html", context={"request": request}
    )


class ReportCreateForm(BaseModel):
    """Form for creating a new report."""

    location: str
    imgpath: str
    desc: str
    severity: Severity


@router.post("/create")
async def create_report_endpoint(
    request: Request, report: Annotated[ReportCreateForm, Form()]
):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")

    pothole = Pothole(
        location=report.location,
        image_path=report.imgpath,
        description=report.desc,
        severity=report.severity,
    )

    success = await create_report(request, pothole)

    if not success:
        pass  # Add some logic in here later

    return HTMLResponse(content=f"Report {report} created!", status_code=201)


class ReportEditForm(BaseModel):
    location: str
    desc: str
    severity: Severity
    status: Status


@router.put("/edit")
async def edit_report_endpoint(
    request: Request, report: Annotated[ReportEditForm, Form()]
):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")

    await edit_report(request, report)


@router.delete("/delete/{report_id}")
async def delete_report_endpoint(request: Request, report_id: int):
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")

    await delete_report(request, report_id)


@router.post("/image-upload")
async def report_image_upload(request: Request, image: UploadFile = File(...)):
    """This is the route to access the image upload form."""
    if not SessionUser.get_session_user(request):
        return RedirectResponse("/login")

    path = ""
    filename = ""
    if image.file and image.filename:
        filename = "temp_" + str(uuid.uuid4()) + "." + image.filename.split(".")[-1]
        path = "./public/uploaded-images/" + filename

        with open(path, "wb") as fp:
            _ = fp.write(await image.read())

    if path == "":
        return RedirectResponse(
            "/"
        )  # This should return an error code for Missing fields

    return templates.TemplateResponse(
        "components/location_upload.html",
        context={"request": request, "img_path": filename},
    )
