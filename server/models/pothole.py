import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field

try:
    from .enums import Status, Severity
except ImportError:
    from enums import Status, Severity

class Pothole(BaseModel):
    id: Annotated[int, Field(default_factory=lambda: uuid.uuid4().int)]
    location: Annotated[str, Field(description="Pothole location")]
    image_path: Annotated[str, Field(description="Pothole image path")]
    description: Annotated[Optional[str], Field(description="Pothole description")]
    status: Annotated[Status, Field(default=Status.REPORTED, description="Pothole status")]
    severity: Annotated[Severity, Field(description="Pothole severity")]
