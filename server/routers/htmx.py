from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/htmx", tags=["HTMX"]) # This router will be specific for serving data to HTMX requesting services.

@router.get("/reports")
async def get_reports(request: Request):
    pass

@router.get("/report/image-upload")
async def report_image_upload(request: Request):
    """This is the route to access the image upload form."""
    pass

@router.get("/report/location-upload")
async def report_location_upload(request: Request):
    """This is the route to access the location upload form."""
    pass

@router.get("/report/success")
async def report_success(request: Request):
    """This is the route to access the report success page on successful upload."""
    pass

@router.get("/report/failure")
async def report_failure(request: Request):
    """This is the route to access the report failure page in case an error occurs while uploading."""
    pass