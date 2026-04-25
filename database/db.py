import sqlite3
from contextlib import contextmanager
from typing import Iterator

from config import DB_PATH
from database.schema import SCHEMA_SQL


class Database:
    def __init__(self, db_path: str | None = None):
        self.db_path = str(db_path or DB_PATH)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize(self) -> None:
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            self._ensure_products_columns(conn)
            self._ensure_stock_movements_columns(conn)
            self._ensure_sales_columns(conn)
            conn.commit()

    def _ensure_products_columns(self, conn: sqlite3.Connection) -> None:
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(products)").fetchall()}
        required = {
            "code": "TEXT",
            "category": "TEXT",
            "purchase_price": "REAL NOT NULL DEFAULT 0",
            "sale_price": "REAL NOT NULL DEFAULT 0",
            "alert_threshold": "INTEGER NOT NULL DEFAULT 5",
        }
        for column, ddl in required.items():
            if column not in existing:
                conn.execute(f"ALTER TABLE products ADD COLUMN {column} {ddl}")

        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_products_code ON products(code)")

        conn.execute(
            """
            UPDATE products
            SET
                code = COALESCE(NULLIF(code, ''), printf('P%05d', id)),
                purchase_price = COALESCE(purchase_price, 0),
                sale_price = COALESCE(sale_price, COALESCE(unit_price, 0)),
                alert_threshold = COALESCE(alert_threshold, COALESCE(min_threshold, 5))
            """
        )

    def _ensure_stock_movements_columns(self, conn: sqlite3.Connection) -> None:
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(stock_movements)").fetchall()}
        if "note" not in existing:
            conn.execute("ALTER TABLE stock_movements ADD COLUMN note TEXT")

    def _ensure_sales_columns(self, conn: sqlite3.Connection) -> None:
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(sales)").fetchall()}
        if "payment_mode" not in existing:
            conn.execute("ALTER TABLE sales ADD COLUMN payment_mode TEXT NOT NULL DEFAULT 'comptant'")

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


db = Database()
