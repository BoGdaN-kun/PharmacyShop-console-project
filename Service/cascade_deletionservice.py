from Domain.cascade_undo_redo import DeleteCascadeOperation
from Repository.repository import Repository
from Service.ClientCardService import ClientCardService
from Service.DrugService import DrugService
from Service.TransactionService import TransactionService
from Service.undo_redo_service import UndoRedoService


class CascadeDeletion:
    def __init__(self, drug_repository: Repository,
                 client_card_repository: Repository,
                 transaction_repository: Repository,
                 drug_service: DrugService,
                 transaction_service: TransactionService,
                 client_card_service: ClientCardService,
                 undo_redo_service: UndoRedoService):

        self.undo_redo_service = undo_redo_service
        self.drug_repository = drug_repository
        self.client_card_repository = client_card_repository
        self.transaction_repository = transaction_repository
        self.drug_service = drug_service
        self.transaction_service = transaction_service
        self.client_card_service = client_card_service

    def delete(self, id_entity: str, entity: str):
        """
        Deletes in cascade
        :param id_entity: id entity
        :param entity: entity type drug/client card
        :return: None
        """
        drug_list = []
        transactions_list = []
        client_card_list = []
        if entity == 'drug':
            if self.drug_repository.read(id_entity):
                drug = self.drug_repository.read(id_entity)
                drug_list.append(drug)
                self.drug_repository.delete(id_entity)
            for transaction in self.transaction_service.get_all():
                if transaction.drug_id == id_entity:
                    transactions_list.append(transaction)
                    self.transaction_service.delete_transaction(
                        transaction.id_entity)
            self.undo_redo_service.clear_redo()
            delete_operation = DeleteCascadeOperation(
                self.drug_repository,
                self.transaction_repository,
                drug_list,
                transactions_list)
            self.undo_redo_service.add_to_undo(delete_operation)

        elif entity == 'client card':
            if self.client_card_repository.read(id_entity):
                client_card = self.client_card_repository.read(id_entity)
                client_card_list.append(client_card)
                self.client_card_repository.delete(id_entity)
            for transaction in self.transaction_service.get_all():
                if transaction.client_card_id == id_entity:
                    transactions_list.append(transaction)
                    self.transaction_service.delete_transaction(
                        transaction.id_entity)
            self.undo_redo_service.clear_redo()
            delete_operation = DeleteCascadeOperation(
                self.client_card_repository, self.transaction_repository,
                client_card_list, transactions_list)
            self.undo_redo_service.add_to_undo(delete_operation)
