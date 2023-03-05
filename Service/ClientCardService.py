from typing import List

from Domain.ClientCard import ClientCard
from Domain.ClientCardValidation import ClientCardValidation
from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class ClientCardService:
    def __init__(self, client_card_repository: Repository,
                 card_client_validator: ClientCardValidation,
                 undo_redo_sercice: UndoRedoService):
        self.client_card_repository = client_card_repository
        self.client_card_validator = card_client_validator
        self.undo_redo_service = undo_redo_sercice

    def add_client_card(self, id_client_card: str, client_name: str,
                        client_first_name: str, client_cnp: str,
                        client_birthdate: str,
                        client_registration_date: str):
        """
        Add a client card
        :param id_client_card:id client card
        :param client_name:client name
        :param client_first_name:client first name
        :param client_cnp:client cnp
        :param client_birthdate: client birthdate
        :param client_registration_date:client registration date
        :return: None
        """
        if len(client_cnp) != 13:
            raise KeyError("CNP must contain 13 figures.")
        client_card = ClientCard(id_client_card, client_name,
                                 client_first_name, client_cnp,
                                 client_birthdate,
                                 client_registration_date)
        self.client_card_validator.validate(client_card)
        if self.client_card_repository.read(id_client_card) is not None:
            raise KeyError("There is already a client card with the id "
                           + id_client_card)

        if self.client_card_repository.read(
                client_card.client_CNP) is not None:
            raise KeyError("There is already a client with this CNP.")
        cards_client = self.get_all()
        cnp_list = []
        for i in cards_client:
            cnp_list.append(getattr(i, "client_CNP"))
        if client_cnp in cnp_list:
            raise ValueError(f"Cnp {client_cnp} already exist.")
        self.client_card_repository.create(client_card)
        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.client_card_repository, client_card)
        self.undo_redo_service.add_to_undo(add_operation)

    def get_all(self) -> List[ClientCard]:
        return self.client_card_repository.read()

    def update_client_card(self, id_client_card: str, client_name: str,
                           client_first_name: str, client_cnp: str,
                           client_birthdate: str,
                           client_registration_date: str):
        """
        Update  client card
        :param id_client_card:id client card
        :param client_name:client name
        :param client_first_name:client first name
        :param client_cnp:client cnp
        :param client_birthdate:client birthdate
        :param client_registration_date:client registration date
        :return:
        """
        if len(client_cnp) != 13:
            raise KeyError("CNP must contain 13 figures.")
        client_card = ClientCard(id_client_card, client_name,
                                 client_first_name, client_cnp,
                                 client_birthdate,
                                 client_registration_date)
        if self.client_card_repository.read(id_client_card) is None:
            msg = f"There isn't any client card with {id_client_card} id."
            raise KeyError(msg)
        else:
            before_update_drug = self.client_card_repository.read(
                id_client_card)
        self.client_card_validator.validate(client_card)
        self.client_card_repository.update(client_card)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.client_card_repository,
                                           before_update_drug, client_card)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_client_card(self, id_client_card: str):
        """
        Delete client card
        :param id_client_card: id client card
        :return:
        """
        client_card_to_delete = self.client_card_repository.read(
            id_client_card)

        self.client_card_repository.delete(id_client_card)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.client_card_repository,
                                           client_card_to_delete)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_id(self, id_client_card: str):
        """
        Returns the object with id
        :param id_client_card: id client card
        :return: Client Card Object
        """
        return self.client_card_repository.read(id_client_card)

    def search(self, text: str):
        """
        Returns a list with ClientCard Objects where text is in
        :param text: text you want to search
        :return: result
        """
        result = []
        client_cards = self.client_card_repository.read()
        for client_card in client_cards:
            if (text in client_card.client_CNP) or (
                    text in client_card.client_name) or (
                    text in client_card.client_birthdate) or (
                    text in client_card.client_registration_date) or (
                    text in client_card.client_first_name):
                result.append(client_card)
        return result
