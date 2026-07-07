CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    internet_plan TEXT,
    autopay INTEGER DEFAULT 0,
    account_status TEXT,
    join_date TEXT
);

CREATE TABLE bills (
    bill_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    due_date TEXT,
    status TEXT,
    last_payment_date TEXT,
    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE network (
    customer_id INTEGER PRIMARY KEY,
    outage INTEGER,
    internet_status TEXT,
    router_status TEXT,
    signal_strength INTEGER,
    last_restart TEXT,
    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
);