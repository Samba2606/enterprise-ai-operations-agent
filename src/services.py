import sqlite3
from typing import Any

from src.config import DATABASE_PATH

def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    return con

def get_customer(customer_id: str) -> dict[str, Any]:
    with _connect() as con:
        row = con.execute(
            "SELECT customer_id, name, email, segment FROM customers WHERE customer_id = ?",
            (customer_id,),
        ).fetchone()

    return dict(row) if row else {"error": "customer not found"}

def get_order(order_id: str) -> dict[str, Any]:
    with _connect() as con:
        row = con.execute(
            """SELECT order_id, customer_id, product, amount, status,
                      promised_date, carrier_status
               FROM orders
               WHERE order_id = ?""",
            (order_id,),
        ).fetchone()

    return dict(row) if row else {"error": "order not found"}

def get_support_history(customer_id: str) -> list[dict[str, Any]]:
    with _connect() as con:
        rows = con.execute(
            """SELECT ticket_id, issue, status, created_at
               FROM tickets
               WHERE customer_id = ?
               ORDER BY created_at DESC""",
            (customer_id,),
        ).fetchall()

    return [dict(row) for row in rows]

def create_ticket(customer_id: str, issue: str) -> dict[str, Any]:
    if not issue.strip():
        return {"error": "issue cannot be empty"}

    with _connect() as con:
        cur = con.execute(
            """INSERT INTO tickets(customer_id, issue, status)
               VALUES (?, ?, 'open')""",
            (customer_id, issue.strip()),
        )
        con.commit()
        ticket_id = f"TKT-{cur.lastrowid:04d}"

    return {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "status": "open",
        "message": "ticket created",
    }
