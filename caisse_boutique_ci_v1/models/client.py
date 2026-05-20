from dataclasses import dataclass


@dataclass
class Client:
    id: int | None
    nom: str
    telephone: str
