from dataclasses import dataclass


@dataclass(slots=True)
class Client:
    id: int | None
    full_name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
