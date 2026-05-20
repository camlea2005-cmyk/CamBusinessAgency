from dataclasses import dataclass


@dataclass
class Dette:
    id: int | None
    client_id: int
    montant: float
    solde: float
