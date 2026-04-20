from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    display_name: str
    timezone: str
    created_at: datetime
