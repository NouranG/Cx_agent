import sqlite3

conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# ------------------------
# Customers
# ------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    region TEXT,
    plan TEXT
)
""")

# ------------------------
# Billing
# ------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS billing(
    customer_id INTEGER,
    balance REAL,
    status TEXT,
    last_payment TEXT,
    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
)
""")

customers = [

(1001,"Alice Johnson","alice@email.com","New York","Premium"),
(1002,"Bob Smith","bob@email.com","California","Basic"),
(1003,"Charlie Brown","charlie@email.com","Texas","Business"),
(1004,"Diana Miller","diana@email.com","Florida","Premium"),
(1005,"Emma Davis","emma@email.com","Washington","Basic")

]

billing = [

(1001,0,"Paid","2026-06-30"),
(1002,45,"Overdue","2026-05-15"),
(1003,120,"Pending","2026-06-01"),
(1004,0,"Paid","2026-06-29"),
(1005,18,"Pending","2026-06-20")

]

cursor.executemany(
    "INSERT OR REPLACE INTO customers VALUES (?,?,?,?,?)",
    customers
)

cursor.executemany(
    "INSERT OR REPLACE INTO billing VALUES (?,?,?,?)",
    billing
)

conn.commit()
conn.close()

print("Database initialized.")