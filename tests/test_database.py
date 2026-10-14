import sqlite3

from database.init_db import initialize_database


def test_initialize_database_creates_expected_tables_and_seed_data(tmp_path):
    db_path = tmp_path / "customers.db"
    initialize_database(db_path)

    with sqlite3.connect(db_path) as conn:
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        assert {"customers", "bills", "network"} <= tables
        customer = conn.execute(
            "SELECT first_name, last_name FROM customers WHERE customer_id = ?",
            (1001,),
        ).fetchone()
        bill = conn.execute(
            "SELECT amount FROM bills WHERE customer_id = ?",
            (1003,),
        ).fetchone()
        network = conn.execute(
            "SELECT internet_status FROM network WHERE customer_id = ?",
            (1002,),
        ).fetchone()

    assert customer == ("Alice", "Johnson")
    assert bill == (120.0,)
    assert network == ("offline",)


def test_initialize_database_can_be_run_twice(tmp_path):
    db_path = tmp_path / "customers.db"
    initialize_database(db_path)
    initialize_database(db_path)
    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    assert count == 5
