from sqlalchemy.orm import Session
from app.classifier import classify_ticket
from app.models import Ticket
from app.schemas import TicketCreate


def create_ticket(db: Session, payload: TicketCreate) -> Ticket:
    result = classify_ticket(payload.message)
    status = "NEEDS_REVIEW" if result["requires_review"] else "PENDING_REVIEW"
    ticket = Ticket(
        ticket_id=payload.ticket_id.strip(),
        message=payload.message.strip(),
        category=result["category"],
        priority=result["priority"],
        assigned_team=result["assigned_team"],
        summary=result["summary"],
        draft_response=result["draft_response"],
        status=status,
        requires_review=result["requires_review"],
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
