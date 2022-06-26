from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class UpdateOperation(UndoRedoOperation):

    def __init__(self, repository: Repository,
                 before_update_entity: Entity,
                 updated_entity: Entity):
        self.repository = repository
        self.before_update_entity = before_update_entity
        self.updated_entity = updated_entity

    def undo(self):
        self.repository.update(self.before_update_entity)

    def redo(self):
        self.repository.update(self.updated_entity)
