from database.db import db


class StockService:
    @staticmethod
    def adjust_stock(product_id: int, quantity_delta: int, movement_type: str, note: str | None = None) -> None:
        if movement_type not in {"IN", "OUT", "ADJUST"}:
            raise ValueError("Type de mouvement invalide")

        with db.transaction() as conn:
            row = conn.execute(
                "SELECT quantity, name FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
            if not row:
                raise ValueError("Produit introuvable")

            new_qty = int(row["quantity"]) + int(quantity_delta)
            if new_qty < 0:
                raise ValueError("Stock insuffisant : opération refusée")

            conn.execute(
                "UPDATE products SET quantity = ? WHERE id = ?",
                (new_qty, product_id),
            )
            conn.execute(
                """
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    product_id,
                    movement_type,
                    abs(int(quantity_delta)),
                    f"Mouvement {movement_type}",
                    note,
                ),
            )

    @staticmethod
    def get_low_stock_products():
        with db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, code, name, quantity, alert_threshold
                FROM products
                WHERE quantity <= alert_threshold
                ORDER BY quantity ASC
                """
            ).fetchall()
