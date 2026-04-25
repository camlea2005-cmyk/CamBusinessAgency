from database.db import db


class ReportService:
    @staticmethod
    def get_monthly_summary(year: int, month: int) -> dict:
        ym = f"{year:04d}-{month:02d}"
        with db.get_connection() as conn:
            sales = conn.execute(
                "SELECT COALESCE(SUM(total_amount), 0) AS t FROM sales WHERE strftime('%Y-%m', created_at) = ?",
                (ym,),
            ).fetchone()["t"]
            expenses = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) AS t FROM expenses WHERE strftime('%Y-%m', expense_date) = ?",
                (ym,),
            ).fetchone()["t"]

        sales = float(sales or 0)
        expenses = float(expenses or 0)
        return {"sales": sales, "expenses": expenses, "profit": sales - expenses}
