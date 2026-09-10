from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Ticket
from schemas import TicketCreate, TicketResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    new_ticket = Ticket(
        category=ticket.category.value,
        priority=ticket.priority.value,
        assigned_team=ticket.assigned_team,
        summary=ticket.summary,
        status=ticket.status.value,
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
    try:
        ticket_number = int(ticket_id.removeprefix("T-"))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket ID",
        )

    ticket = db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket
