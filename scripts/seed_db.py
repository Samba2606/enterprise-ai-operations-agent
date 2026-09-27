from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "enterprise.db"
DB.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB) as con:
    con.executescript("""
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS tickets;

    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        segment TEXT NOT NULL
    );

    CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        product TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        promised_date TEXT NOT NULL,
        carrier_status TEXT NOT NULL
    );

    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        customer_id TEXT NOT NULL,
        issue TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    con.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)",
        [
            ("CUST-001", "Asha Rao", "asha@example.com", "gold"),
            ("CUST-002", "Rohan Das", "rohan@example.com", "standard"),
            ("CUST-003", "Meera Shah", "meera@example.com", "gold"),
        ],
    )

    con.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "ORD-1001",
                "CUST-001",
                "Wireless Keyboard",
                3499,
                "delivered",
                "2026-09-18",
                "delivered 2026-09-17",
            ),
            (
                "ORD-1002",
                "CUST-002",
                "Noise Cancelling Headphones",
                8999,
                "delayed",
                "2026-09-15",
                "carrier delay; no confirmed delivery date",
            ),
            (
                "ORD-1003",
                "CUST-003",
                "Mechanical Keyboard",
                6499,
                "in_transit",
                "2026-09-30",
                "in transit",
            ),
        ],
    )

    con.executemany(
        """INSERT INTO tickets(ticket_id, customer_id, issue, status)
           VALUES (?, ?, ?, ?)""",
        [
            (
                "TKT-0001",
                "CUST-002",
                "Asked for order status",
                "closed",
            ),
            (
                "TKT-0002",
                "CUST-002",
                "Carrier delay complaint",
                "open",
            ),
        ],
    )

    con.commit()

print(f"Seeded demo database: {DB}")
