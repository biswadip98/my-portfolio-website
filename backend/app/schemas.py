from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    """Shape of an incoming contact-form submission."""

    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(min_length=1, max_length=5000)


class ContactResponse(BaseModel):
    """Shape of the contact message we send back to the client."""

    id: int
    name: str
    email: EmailStr
    message: str
    created_at: datetime

    # Allows creating this schema directly from a SQLAlchemy model object.
    model_config = {"from_attributes": True}


class VisitResponse(BaseModel):
    """Shape of the visitor-counter response."""

    count: int
