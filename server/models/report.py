import uuid
from datetime import datetime as dt
from typing import Annotated
from pydantic import BaseModel, Field

from .enums import Status, Severity


class Report(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: str(uuid.uuid4()))]
    location: Annotated[str, Field(description="Report location")]
    image_path: Annotated[str, Field(description="Report image path")]
    description: Annotated[str, Field(description="Report description")]
    status: Annotated[
        Status, Field(default=Status.REPORTED, description="Report status")
    ]
    severity: Annotated[Severity, Field(description="Report severity")]
    created_at: Annotated[
        str,
        Field(
            default_factory=lambda: dt.now().strftime("%Y-%m-%d"),
            description="Date report was created",
        ),
    ]
    updated_at: Annotated[
        str,
        Field(
            default_factory=lambda: dt.now().strftime("%Y-%m-%d"),
            description="Date report was last updated",
        ),
    ]
    user_email: Annotated[
        str, Field(default="", description="The email of the uploader")
    ]

    class Config:
        use_enum_values: bool = True
