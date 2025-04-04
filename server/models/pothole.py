import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from enums import Status, Severity

class Pothole(BaseModel):
    id: Annotated[int, Field(default_factory=lambda: uuid.uuid4().int)]
    lattitude: Annotated[float, Field(description="Pothole lattitude")]
    longitude: Annotated[float, Field(description="Pothole longitude")]
    address: Annotated[str, Field(description="Pothole address")]
    image_path: Annotated[str, Field(description="Pothole image path")]
    description: Annotated[Optional[str], Field(description="Pothole description")]
    status: Annotated[Status, Field(default=Status.REPORTED, description="Pothole status")]
    servity: Annotated[Severity, Field(description="Pothole severity")]