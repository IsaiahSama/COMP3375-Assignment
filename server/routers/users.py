from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from services.report_services import create_report
from models.pothole import Pothole
from typing import Annotated
from pydantic import BaseModel
from models.enums import Severity

router = APIRouter()
class ReportCreateForm(BaseModel):
    """Form for creating a new report."""
    lattitude: float
    longitude: float
    address: str
    image_path: str
    description: str
    severity: Severity

@router.post("/report/create")
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