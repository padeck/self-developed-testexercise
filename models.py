from sqlalchemy import Sequence, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

ticket_id_sequence = Sequence("ticket_id_sequence", start=1001)


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_number: Mapped[int] = mapped_column(
        ticket_id_sequence,
        primary_key=True,
        server_default=ticket_id_sequence.next_value(),
    )

    category: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(20))
    assigned_team: Mapped[str] = mapped_column(String(100))
    summary: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50))

    @property
    def ticket_id(self) -> str:
        return f"T-{self.ticket_number}"
