from fastapi import Request
from server.models.pothole import Pothole

async def create_report(request: Request, report: Pothole) -> bool:
    """Create a new report."""
    pass

async def edit_report(request: Request, report: Pothole) -> bool:
    """Edit an existing report."""
    pass

async def delete_report(request: Request, report: int) -> bool:
    """Delete a report."""
    pass

