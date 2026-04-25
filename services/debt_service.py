from database.db import db


class DebtService:
    @staticmethod
    def list_debts():
        with db.get_connection() as conn:
            return conn.execute(
                """
                SELECT d.id, c.full_name, d.amount, d.status, d.due_date
                FROM client_debts d
                JOIN clients c ON c.id = d.client_id
                ORDER BY d.created_at DESC
                """
            ).fetchall()
