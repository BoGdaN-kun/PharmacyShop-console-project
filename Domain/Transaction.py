from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Transaction(Entity):
    drug_id: str
    client_card_id: str
    number_of_pieces: int
    date_and_hour: str
