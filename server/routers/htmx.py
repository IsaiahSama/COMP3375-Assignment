from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/htmx", tags=["HTMX"]) # This router will be specific for serving data to HTMX requesting services.

templates = Jinja2Templates(directory="templates")

@router.get("/reports")
async def get_reports(request: Request):
    pass

@router.get("/report/image-upload")
async def report_image_upload(request: Request):
    """This is the route to access the image upload form."""
    return templates.TemplateResponse("components/image_upload.html", context={"request": request})

@router.get("/report/location-upload")
async def report_location_upload(request: Request):
    """This is the route to access the location upload form."""
    return templates.TemplateResponse("components/location_upload.html", context={"request": request})

@router.get("/report/success")
async def report_success(request: Request):
    """This is the route to access the report success page on successful upload."""
    return templates.TemplateResponse("components/upload_result.html", context={"request": request, "result": "Success!", "message": "Your report has been submitted!"})

@router.get("/report/failure")
async def report_failure(request: Request):
    """This is the route to access the report failure page in case an error occurs while uploading."""
    return templates.TemplateResponse("components/upload_result.html", context={"request": request, "result": "Failed!", "message": "Your report could not be uploaded. Try again later"})
