from dataclasses import dataclass


@dataclass
class Produit:
    id: int | None
    nom: str
    prix: float
    stock: int
