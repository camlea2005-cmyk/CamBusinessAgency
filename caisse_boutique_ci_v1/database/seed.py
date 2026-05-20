"""Initialisation de données de test."""

from database.db import get_connection


def seed():
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO produits (nom, prix, stock) VALUES (?, ?, ?)",
            ("Produit exemple", 1000, 10),
        )
