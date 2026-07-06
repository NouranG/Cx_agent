import sqlite3

DB_PATH = "database/customers.db"


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def get_customer(self, customer_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM customers
            WHERE customer_id=?
            """,
            (customer_id,)
        )

        return cursor.fetchone()

    def get_billing(self, customer_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM billing
            WHERE customer_id=?
            """,
            (customer_id,)
        )

        return cursor.fetchone()

    def close(self):
        self.conn.close()