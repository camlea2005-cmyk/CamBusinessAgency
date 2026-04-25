from database.db import db


class SalesService:
    @staticmethod
    def create_sale(client_id: int | None, total_amount: float, paid_amount: float, debt_amount: float, notes: str | None = None) -> int:
        with db.transaction() as conn:
            cur = conn.execute(
                """
                INSERT INTO sales (client_id, total_amount, paid_amount, debt_amount, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (client_id, total_amount, paid_amount, debt_amount, notes),
            )
            return int(cur.lastrowid)
