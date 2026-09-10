from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(TicketCreate):
    id: str
