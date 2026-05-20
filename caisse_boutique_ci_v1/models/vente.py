from dataclasses import dataclass


@dataclass
class Vente:
    id: int | None
    client_id: int | None
    total: float
