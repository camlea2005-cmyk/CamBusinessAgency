from database.db import db


class ExpenseService:
    @staticmethod
    def create_expense(label: str, amount: float, category: str | None = None, notes: str | None = None) -> int:
        with db.transaction() as conn:
            cur = conn.execute(
                "INSERT INTO expenses (label, amount, category, notes) VALUES (?, ?, ?, ?)",
                (label, amount, category, notes),
            )
            return int(cur.lastrowid)
