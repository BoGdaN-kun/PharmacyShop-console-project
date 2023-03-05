from abc import ABC
from dataclasses import dataclass


# We made this abstract class because we want to make sure that all the entities have an id
@dataclass
class Entity(ABC):
    id_entity: str
