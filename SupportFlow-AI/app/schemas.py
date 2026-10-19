from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    ticket_id: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=5, max_length=5000)
    model_config = ConfigDict(str_strip_whitespace=True)


class TicketResponse(BaseModel):
    ticket_id: str
    message: str
    category: str
    priority: str
    assigned_team: str
    summary: str
    draft_response: str
    status: str
    requires_review: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
