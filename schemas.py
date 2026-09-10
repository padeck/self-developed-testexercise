from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TicketCategory(str, Enum):
    incident = "incident"
    request = "request"
    problem = "problem"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"
    manual_review_required = "manual_review_required"


class AssignedTeam(str, Enum):
    platform_operations = "platform-operations"
    customer_support = "customer-support"
    security = "security"
    networking = "networking"
    database = "database"


class TicketCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class TicketResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    ticket_id: str = Field(alias="ticketId")
    category: TicketCategory
    priority: TicketPriority
    assigned_team: str = Field(alias="assignedTeam")
    summary: str
    status: TicketStatus


class TicketClassification(BaseModel):
    category: TicketCategory
    priority: TicketPriority
    assigned_team: AssignedTeam
    summary: str
    status: TicketStatus
