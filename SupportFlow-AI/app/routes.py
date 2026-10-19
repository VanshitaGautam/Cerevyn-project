from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket
from app.schemas import TicketCreate, TicketResponse
from app.services import create_ticket

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(payload: TicketCreate, db: Session = Depends(get_db)):
    try:
        return create_ticket(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A ticket with this ID already exists.",
        )


@router.get("", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket


@router.post("/{ticket_id}/approve", response_model=TicketResponse)
def approve_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    if ticket.status == "READY":
        raise HTTPException(status_code=409, detail="This ticket has already been approved.")

    # Human approval is required before a ticket is marked READY.
    ticket.status = "READY"
    ticket.requires_review = False
    db.commit()
    db.refresh(ticket)
    return ticket
