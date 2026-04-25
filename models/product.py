from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    id: int | None
    code: str
    name: str
    category: str | None
    purchase_price: float
    sale_price: float
    quantity: int
    alert_threshold: int = 5
