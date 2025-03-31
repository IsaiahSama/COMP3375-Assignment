from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/htmx", tags=["HTMX"]) # This router will be specific for serving data to HTMX requesting services.

@router.get("/hello")
async def hello():
    return HTMLResponse(content="Hello from HTMX!", status_code=200)
