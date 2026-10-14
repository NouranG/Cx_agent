import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("customers.db")
SCHEMA_PATH = Path(__file__).with_name("scheme.sql")


def initialize_database(db_path: str | Path = DATABASE_PATH) -> None:
    """Create the project schema and insert deterministic demo records."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    customers = [
        (1001, "Alice", "Johnson", "alice@example.com", "555-0101", "10 Main St", "New York", "NY", "10001", "Premium", 1, "active", "2025-01-10"),
        (1002, "Bob", "Smith", "bob@example.com", "555-0102", "20 Oak St", "Los Angeles", "CA", "90001", "Basic", 0, "active", "2025-02-15"),
        (1003, "Charlie", "Brown", "charlie@example.com", "555-0103", "30 Pine St", "Austin", "TX", "73301", "Business", 0, "suspended", "2024-11-05"),
        (1004, "Diana", "Miller", "diana@example.com", "555-0104", "40 Lake St", "Miami", "FL", "33101", "Premium", 1, "active", "2025-03-20"),
        (1005, "Emma", "Davis", "emma@example.com", "555-0105", "50 Hill St", "Seattle", "WA", "98101", "Basic", 0, "active", "2025-04-02"),
    ]
    bills = [
        (1, 1001, 0.0, "2026-11-01", "paid", "2026-10-01"),
        (2, 1002, 45.0, "2026-10-20", "overdue", "2026-08-15"),
        (3, 1003, 120.0, "2026-10-20", "overdue", "2026-08-01"),
        (4, 1004, 0.0, "2026-11-03", "paid", "2026-10-03"),
        (5, 1005, 18.0, "2026-10-25", "pending", "2026-09-20"),
    ]
    networks = [
        (1001, 0, "online", "online", 92, "2026-10-01"),
        (1002, 0, "offline", "online", 48, "2026-10-10"),
        (1003, 1, "offline", "offline", 15, "2026-10-08"),
        (1004, 0, "online", "online", 87, "2026-10-02"),
        (1005, 0, "online", "online", 75, "2026-10-04"),
    ]

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)
        conn.executemany(
            """
            INSERT OR REPLACE INTO customers
            (customer_id, first_name, last_name, email, phone, address, city,
             state, zip_code, internet_plan, autopay, account_status, join_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            customers,
        )
        conn.executemany(
            """
            INSERT OR REPLACE INTO bills
            (bill_id, customer_id, amount, due_date, status, last_payment_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            bills,
        )
        conn.executemany(
            """
            INSERT OR REPLACE INTO network
            (customer_id, outage, internet_status, router_status, signal_strength, last_restart)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            networks,
        )


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at {DATABASE_PATH}")
