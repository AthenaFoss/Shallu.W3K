import sqlite3
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4
from fastapi import APIRouter, HTTPException

# Support Ticket Model
class SupportTicket(BaseModel):
    question: str

# Connect to the SQLite database
conn = sqlite3.connect('databases/support-ticket/support-ticket.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS support_tickets
                  (id TEXT PRIMARY KEY, question TEXT)''')

# Function to add a new support ticket
def add_support_ticket(question: str) -> str:
    ticket_id = str(uuid4())
    cursor.execute("INSERT INTO support_tickets (id, question) VALUES (?, ?)", (ticket_id, question))
    conn.commit()
    return ticket_id

# Function to get a support ticket by ID
def get_support_ticket(ticket_id: str) -> Optional[SupportTicket]:
    cursor.execute("SELECT question FROM support_tickets WHERE id = ?", (ticket_id,))
    result = cursor.fetchone()
    if result:
        question = result[0]
        return SupportTicket(question=question)
    return None

# Function to list all support tickets with pagination
def list_support_tickets(page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    cursor.execute("SELECT id, question FROM support_tickets LIMIT ? OFFSET ?", (page_size, offset))
    results = cursor.fetchall()
    return [SupportTicket(question=question) for id, question in results]

# Function to close (delete) a support ticket
def close_support_ticket(ticket_id: str):
    cursor.execute("DELETE FROM support_tickets WHERE id = ?", (ticket_id,))
    conn.commit()

# Support Ticket Router
support_ticket_router = APIRouter(prefix="/support-ticket")

@support_ticket_router.post("/add")
def add_ticket(ticket: SupportTicket):
    try:
        ticket_id = add_support_ticket(ticket.question)
        return {"message": "Ticket added successfully", "ticket_id": ticket_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@support_ticket_router.get("/list")
def get_tickets(page: int = 1, page_size: int = 10):
    try:
        tickets = list_support_tickets(page, page_size)
        return {"tickets": tickets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@support_ticket_router.get("/list/{ticket_id}")
def get_ticket(ticket_id: str):
    try:
        ticket = get_support_ticket(ticket_id)
        if ticket:
            return ticket
        else:
            raise HTTPException(status_code=404, detail="Ticket not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@support_ticket_router.delete("/close/{ticket_id}")
def close_ticket(ticket_id: str):
    try:
        close_support_ticket(ticket_id)
        return {"message": "Ticket closed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))