from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class DeleteIntervalOperation(UndoRedoOperation):

    def __init__(self, repository: Repository,
                 deleted_entities: List[Entity]):
        self.repository = repository
        self.deleted_entities = deleted_entities

    def undo(self):
        for i in self.deleted_entities:
            self.repository.create(i)

    def redo(self):
        for i in self.deleted_entities:
            self.repository.delete(i.id_entity)
