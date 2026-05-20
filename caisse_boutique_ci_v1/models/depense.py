from dataclasses import dataclass


@dataclass
class Depense:
    id: int | None
    libelle: str
    montant: float
