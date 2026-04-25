from database.db import db


class ClientService:
    @staticmethod
    def list_clients():
        with db.get_connection() as conn:
            return conn.execute("SELECT id, full_name, phone, email FROM clients ORDER BY full_name").fetchall()
