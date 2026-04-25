from database.db import db


class DashboardService:
    @staticmethod
    def get_kpis() -> dict:
        with db.get_connection() as conn:
            products = conn.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]
            stock_value = conn.execute(
                "SELECT COALESCE(SUM(quantity * COALESCE(sale_price, unit_price, 0)), 0) AS v FROM products"
            ).fetchone()["v"]
            sales_today = conn.execute(
                "SELECT COALESCE(SUM(total_amount), 0) AS t FROM sales WHERE date(created_at) = date('now')"
            ).fetchone()["t"]
            expenses_today = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) AS t FROM expenses WHERE expense_date = date('now')"
            ).fetchone()["t"]

        return {
            "products": products,
            "stock_value": float(stock_value or 0),
            "sales_today": float(sales_today or 0),
            "expenses_today": float(expenses_today or 0),
        }
