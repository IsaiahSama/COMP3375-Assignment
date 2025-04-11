from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from server.services.report_services import (
    create_report,
    edit_report,
    delete_report,
    get_all_reports,
)
from server.models.pothole import Pothole
from typing import Annotated
from pydantic import BaseModel
from server.models.enums import Severity, Status

import uuid

router = APIRouter(prefix="/reports", tags=["Reports"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def reports_page(request: Request):
    reports = await get_all_reports(request)

    for report in reports:
        report["image_path"] = report["image_path"].lstrip("./")

    return templates.TemplateResponse(
        "reports/report.html", context={"request": request, "reports": reports}
    )


@router.get("/edit")
async def edit_report_page(request: Request):
    return templates.TemplateResponse("reports/edit.html", context={"request": request})


@router.get("/create")
async def create_report_page(request: Request):
    return templates.TemplateResponse(
        "reports/create.html", context={"request": request}
    )


@router.get("/delete")
async def delete_report_page(request: Request):
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
    """Create a new report."""
    # Assuming report is a JSON string that can be converted to a Pothole object
    pothole = Pothole(
        location=report.location,
        image_path=report.imgpath,
        description=report.desc,
        severity=report.severity,
    )

    await create_report(request, pothole)
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
    edit_report(request, report)


@router.delete("/delete/{report_id}")
async def delete_report_endpoint(request: Request, report_id: int):
    delete_report(request, report_id)


@router.post("/image-upload")
async def report_image_upload(request: Request, image: UploadFile = File(...)):
    """This is the route to access the image upload form."""
    path = ""
    filename = ""
    if image.file and image.filename:
        filename = "temp_" + str(uuid.uuid4()) + "." + image.filename.split(".")[-1]
        path = "./public/uploaded-images/" + filename

        with open(path, "wb") as fp:
            _ = fp.write(await image.read())

    if path == "":
        return RedirectResponse("/")

    return templates.TemplateResponse(
        "components/location_upload.html",
        context={"request": request, "img_path": filename},
    )
