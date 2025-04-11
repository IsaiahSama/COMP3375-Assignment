import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from bson import ObjectId

try:
    from .enums import Roles
except ImportError:
    from enums import Roles

class User(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: str(ObjectId()), description="User ID")]
    role: Annotated[Roles, Field(default=Roles.USER, description="User role")]
    email: Annotated[str, Field(description="User email")]
    password: Annotated[str, Field(description="User password")]
    first_name: Annotated[str, Field(description="User first name")]
    last_name: Annotated[Optional[str], Field(None, description="User last name")]


