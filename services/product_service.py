from collections.abc import Sequence

from database.db import db


class ProductService:
    @staticmethod
    def create_product(
        code: str,
        name: str,
        category: str | None,
        purchase_price: float,
        sale_price: float,
        quantity: int,
        alert_threshold: int,
    ) -> int:
        query = """
        INSERT INTO products (
            code, name, category, purchase_price, sale_price,
            quantity, alert_threshold, sku, unit_price, min_threshold
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cleaned_code = code.strip().upper()
        cleaned_name = name.strip()
        with db.transaction() as conn:
            cursor = conn.execute(
                query,
                (
                    cleaned_code,
                    cleaned_name,
                    category or None,
                    purchase_price,
                    sale_price,
                    quantity,
                    alert_threshold,
                    cleaned_code,
                    sale_price,
                    alert_threshold,
                ),
            )
            return int(cursor.lastrowid)

    @staticmethod
    def update_product(
        product_id: int,
        code: str,
        name: str,
        category: str | None,
        purchase_price: float,
        sale_price: float,
        alert_threshold: int,
    ) -> None:
        query = """
        UPDATE products
        SET
            code = ?,
            name = ?,
            category = ?,
            purchase_price = ?,
            sale_price = ?,
            alert_threshold = ?,
            sku = ?,
            unit_price = ?,
            min_threshold = ?
        WHERE id = ?
        """
        cleaned_code = code.strip().upper()
        with db.transaction() as conn:
            conn.execute(
                query,
                (
                    cleaned_code,
                    name.strip(),
                    category or None,
                    purchase_price,
                    sale_price,
                    alert_threshold,
                    cleaned_code,
                    sale_price,
                    alert_threshold,
                    product_id,
                ),
            )

    @staticmethod
    def delete_product(product_id: int) -> None:
        with db.transaction() as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))

    @staticmethod
    def list_products(search: str | None = None) -> Sequence:
        base_query = """
        SELECT
            id,
            code,
            name,
            category,
            purchase_price,
            sale_price,
            quantity,
            alert_threshold,
            CASE WHEN quantity <= alert_threshold THEN 'ALERTE' ELSE 'OK' END AS status
        FROM products
        """
        params: tuple = ()
        if search and search.strip():
            term = f"%{search.strip()}%"
            base_query += " WHERE code LIKE ? OR name LIKE ? OR COALESCE(category, '') LIKE ? "
            params = (term, term, term)
        base_query += " ORDER BY name"

        with db.get_connection() as conn:
            return conn.execute(base_query, params).fetchall()

    @staticmethod
    def get_product(product_id: int):
        with db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, code, name, category, purchase_price, sale_price, quantity, alert_threshold
                FROM products
                WHERE id = ?
                """,
                (product_id,),
            ).fetchone()
