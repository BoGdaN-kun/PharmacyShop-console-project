from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class ClientCard(Entity):
    client_name: str
    client_first_name: str
    client_CNP: str
    client_birthdate: str
    client_registration_date: str
