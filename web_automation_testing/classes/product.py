from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class Product:
    label: str
    description: str
    price: Union[float, str]
    quantity: int = 1