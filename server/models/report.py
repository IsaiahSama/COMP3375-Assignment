import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field

from .enums import Status, Severity


class Report(BaseModel):
    id: Annotated[int, Field(default_factory=lambda: uuid.uuid4().int)]
    location: Annotated[str, Field(description="Report location")]
    image_path: Annotated[str, Field(description="Report image path")]
    description: Annotated[Optional[str], Field(description="Report description")]
    status: Annotated[
        Status, Field(default=Status.REPORTED, description="Report status")
    ]
    severity: Annotated[Severity, Field(description="Report severity")]
    user_email: Annotated[
        str, Field(default="", description="The email of the uploader")
    ]

    class Config:
        use_enum_values = True
