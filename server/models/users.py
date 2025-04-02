import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from enums import Roles

class User(BaseModel):
    id: Annotated[int, Field(default_factory=lambda: uuid.uuid4().int, description="User ID")]
    role: Annotated[Roles, Field(default=Roles.USER, description="User role")]
    email: Annotated[str, Field(description="User email")]
    password: Annotated[str, Field(description="User password")]
    first_name: Annotated[str, Field(description="User first name")]
    last_name: Annotated[Optional[str], Field(None, description="User last name")]


