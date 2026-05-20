"""Définition du schéma de base."""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);
"""
