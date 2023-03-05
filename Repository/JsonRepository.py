from typing import Dict, Union, Optional, List, Type

import jsonpickle

from Domain.entity import Entity
from Repository.exceptions import DuplicateIdError, NoSuchIdError
from Repository.repository import Repository


class RepositoryJson(Repository):

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Entity]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects, indent=4))

    def create(self, entity: Entity) -> None:
        """
        Creates a new entity in the repository.
        :param entity: the entity to be created
        :return: None
        """

        # self.storage = self.__read_file()
        # super().create(entity)
        # self.__write_file(self.storage)

        entities = self.__read_file()
        if self.read(entity.id_entity) is not None:
            raise DuplicateIdError(f'Already exists an entity with id {entity.id_entity}.')

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def read(self, id_entity: object = None) -> Type[Union[Optional[Entity],
                                                           List[Entity]]]:
        """
        Reads an entity from the repository.
        :param id_entity: the id of the entity to be read
        :return: the entity with id=id_entity or None if id_entity is None
                    or a list with all the entities if id_entity is None
        """

        entities = self.__read_file()
        if id_entity:
            if id_entity in entities:
                return entities[id_entity]
            else:
                return None

        return list(entities.values())

    def update(self, entity: Entity) -> None:
        """
        Updates an entity in the repository.
        :param entity: the entity to be updated
        :return: None
        """

        entities = self.__read_file()
        if self.read(entity.id_entity) is None:
            msg = f'There is no entity with id ' \
                  f'{entity.id_entity} to be updated.'
            raise NoSuchIdError(msg)

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def delete(self, id_entity: str) -> None:
        """
        Deletes an entity from the repository.
        :param id_entity: the id of the entity to be deleted
        :return: None
        """
        entities = self.__read_file()
        if self.read(id_entity) is None:
            raise NoSuchIdError(
                f'There is no entity with id  '
                f'{id_entity} to be deleted.')

        del entities[id_entity]
        self.__write_file(entities)
