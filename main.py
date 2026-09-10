from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Ticket
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(TicketCreate):
    id: str


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@app.get("/tickets", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket
