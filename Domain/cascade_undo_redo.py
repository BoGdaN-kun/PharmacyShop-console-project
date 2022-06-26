from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class DeleteCascadeOperation(UndoRedoOperation):

    def __init__(self, repository1: Repository,
                 repository2: Repository,
                 deleted_entities_rep1: List[Entity],
                 deleted_entities_rep2: List[Entity]):
        self.repository1 = repository1
        self.repository2 = repository2
        self.deleted_entities_rep1 = deleted_entities_rep1
        self.deleted_entities_rep2 = deleted_entities_rep2

    def undo(self):
        for i in self.deleted_entities_rep1:
            self.repository1.create(i)
        for i in self.deleted_entities_rep2:
            self.repository2.create(i)

    def redo(self):
        for i in self.deleted_entities_rep1:
            self.repository1.delete(i.id_entity)
        for i in self.deleted_entities_rep2:
            self.repository2.delete(i.id_entity)
