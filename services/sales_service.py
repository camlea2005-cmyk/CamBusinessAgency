from database.db import db


class SalesService:
    PAYMENT_MODES = {"comptant", "mobile money", "dette"}

    @staticmethod
    def _find_or_create_client(conn, client_name: str | None) -> int | None:
        if not client_name or not client_name.strip():
            return None
        name = client_name.strip()
        row = conn.execute("SELECT id FROM clients WHERE lower(full_name) = lower(?)", (name,)).fetchone()
        if row:
            return int(row["id"])

        cur = conn.execute("INSERT INTO clients (full_name) VALUES (?)", (name,))
        return int(cur.lastrowid)

    @staticmethod
    def list_sales(search: str | None = None):
        query = """
        SELECT
            s.id,
            s.created_at,
            p.name AS product_name,
            si.quantity,
            si.unit_price,
            si.line_total,
            COALESCE(c.full_name, '-') AS client_name,
            s.payment_mode
        FROM sales s
        JOIN sale_items si ON si.sale_id = s.id
        JOIN products p ON p.id = si.product_id
        LEFT JOIN clients c ON c.id = s.client_id
        """
        params: tuple = ()
        if search and search.strip():
            term = f"%{search.strip()}%"
            query += " WHERE p.name LIKE ? OR COALESCE(c.full_name, '') LIKE ? OR s.payment_mode LIKE ? "
            params = (term, term, term)

        query += " ORDER BY s.id DESC"

        with db.get_connection() as conn:
            return conn.execute(query, params).fetchall()

    @staticmethod
    def create_sale(
        product_id: int,
        quantity: int,
        unit_price: float,
        payment_mode: str,
        client_name: str | None = None,
        note: str | None = None,
    ) -> int:
        if quantity <= 0:
            raise ValueError("La quantité doit être supérieure à 0")
        if payment_mode not in SalesService.PAYMENT_MODES:
            raise ValueError("Mode de paiement invalide")

        with db.transaction() as conn:
            product = conn.execute(
                "SELECT id, name, quantity FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
            if not product:
                raise ValueError("Produit introuvable")
            if int(product["quantity"]) < quantity:
                raise ValueError("Stock insuffisant pour valider la vente")

            client_id = SalesService._find_or_create_client(conn, client_name)
            line_total = float(unit_price) * int(quantity)
            paid_amount = line_total if payment_mode != "dette" else 0.0
            debt_amount = line_total - paid_amount

            if payment_mode == "dette" and not client_id:
                raise ValueError("Un client est obligatoire pour une vente à dette")

            sale_cur = conn.execute(
                """
                INSERT INTO sales (client_id, total_amount, paid_amount, debt_amount, payment_mode, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (client_id, line_total, paid_amount, debt_amount, payment_mode, note),
            )
            sale_id = int(sale_cur.lastrowid)

            conn.execute(
                """
                INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, line_total)
                VALUES (?, ?, ?, ?, ?)
                """,
                (sale_id, product_id, quantity, unit_price, line_total),
            )

            new_qty = int(product["quantity"]) - quantity
            conn.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, product_id))
            conn.execute(
                """
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason, note)
                VALUES (?, 'OUT', ?, ?, ?)
                """,
                (product_id, quantity, "Vente", note),
            )

            if payment_mode == "dette":
                conn.execute(
                    """
                    INSERT INTO client_debts (client_id, sale_id, amount, status)
                    VALUES (?, ?, ?, 'UNPAID')
                    """,
                    (client_id, sale_id, debt_amount),
                )

            return sale_id

    @staticmethod
    def delete_sale(sale_id: int) -> None:
        with db.transaction() as conn:
            item = conn.execute(
                "SELECT product_id, quantity FROM sale_items WHERE sale_id = ?",
                (sale_id,),
            ).fetchone()
            if not item:
                raise ValueError("Vente introuvable")

            conn.execute(
                "UPDATE products SET quantity = quantity + ? WHERE id = ?",
                (item["quantity"], item["product_id"]),
            )
            conn.execute(
                """
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason, note)
                VALUES (?, 'IN', ?, 'Annulation vente', 'Suppression vente')
                """,
                (item["product_id"], item["quantity"]),
            )
            conn.execute("DELETE FROM client_debts WHERE sale_id = ?", (sale_id,))
            conn.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
