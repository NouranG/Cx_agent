import sqlite3
from pathlib import Path


DATABASE = Path("database/customers.db")


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE)
        self.conn.row_factory = sqlite3.Row

    def get_customer(self, customer_id):

        cursor = self.conn.execute(
            "SELECT * FROM customers WHERE customer_id=?",
            (customer_id,),
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def get_bill(self, customer_id):

        cursor = self.conn.execute(
            "SELECT * FROM bills WHERE customer_id=?",
            (customer_id,),
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def get_network_status(self, customer_id):

        cursor = self.conn.execute(
            "SELECT * FROM network WHERE customer_id=?",
            (customer_id,),
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def enable_autopay(self, customer_id):

        self.conn.execute(
            """
            UPDATE customers
            SET autopay=1
            WHERE customer_id=?
            """,
            (customer_id,),
        )

        self.conn.commit()

    def disable_autopay(self, customer_id):

        self.conn.execute(
            """
            UPDATE customers
            SET autopay=0
            WHERE customer_id=?
            """,
            (customer_id,),
        )

        self.conn.commit()

    def close(self):

        self.conn.close()