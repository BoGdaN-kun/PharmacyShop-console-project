from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Drug(Entity):
    drug_name: str
    drug_producer: str
    drug_price: float
    need_recipe: str
