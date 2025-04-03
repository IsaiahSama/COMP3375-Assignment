from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from server.services.report_services import create_report
from server.models.pothole import Pothole
from typing import Annotated
from pydantic import BaseModel
from server.models.enums import Severity

router = APIRouter(prefix="/reports", tags=["Reports"])

templates = Jinja2Templates(directory="templates/reports")

@router.get("/")
async def reports_page(request: Request):
    return templates.TemplateResponse("report.html", context={"request": request})

@router.get("/edit")
async def edit_report_page(request: Request):
    return templates.TemplateResponse("edit.html", context={"request": request})

@router.get("/create")
async def create_report_page(request: Request):
    return templates.TemplateResponse("create.html", context={"request": request})

@router.get("/delete")
async def delete_report_page(request: Request):
    return templates.TemplateResponse("delete.html", context={"request": request})


class ReportCreateForm(BaseModel):
    """Form for creating a new report."""
    lattitude: float
    longitude: float
    address: str
    image_path: str
    description: str
    severity: Severity

@router.post("/create")
async def create_report_endpoint(request: Request, report: Annotated[ReportCreateForm, Form()],):
    """Create a new report."""
    # Assuming report is a JSON string that can be converted to a Pothole object
    report = Pothole()
    report.id = ReportCreateForm.id
    report.lattitude = ReportCreateForm.lattitude
    report.longitude = ReportCreateForm.longitude
    report.address = ReportCreateForm.address
    report.image_path = ReportCreateForm.image_path
    report.description = ReportCreateForm.description
    report.severity = ReportCreateForm.severity
    create_report(report)
    return HTMLResponse(content=f"Report {report} created!", status_code=200)

@router.put("/edit")
async def edit_report(request: Request):
    pass 

@router.delete("/delete")
async def delete_report(request: Request):
    pass