import datetime
import time
from typing import List, Union

from Domain.Transaction import Transaction
from Domain.TransactionValidation import TransactionValidation
from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.interval_undo_redo_delete import DeleteIntervalOperation
from Domain.update_operation import UpdateOperation
from ModelView.ModelView import DrugsNoSales
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from utils import my_sorted


class TransactionService:
    def __init__(self,
                 transaction_repository: Repository,
                 drug_repository: Repository,
                 client_card_repository: Repository,
                 transaction_validator: TransactionValidation,
                 undo_redo_service: UndoRedoService
                 ):
        self.transaction_repository = transaction_repository
        self.drug_repository = drug_repository
        self.client_card_repository = client_card_repository
        self.transaction_validator = transaction_validator
        self.undo_redo_service = undo_redo_service

    def add_transaction(self, id_transaction: str, drug_id: str,
                        client_card_id: str, number_of_pieces: int,
                        date_and_hour: str) -> None:
        """
        Adds a new transaction
        :param id_transaction: id transaction
        :param drug_id: drug id
        :param client_card_id: client card id
        :param number_of_pieces: number of pieces
        :param date_and_hour: date and hour
        :return:
        """

        transaction = Transaction(id_transaction, drug_id,
                                  client_card_id,
                                  number_of_pieces,
                                  date_and_hour)
        self.transaction_validator.validate(transaction)
        # print(self.transaction_repository.read(id_transaction))
        if self.transaction_repository.read(id_transaction) is not None:
            raise KeyError("There is already a transaction with"
                           " the id {0}".format(id_transaction))
        if self.drug_repository.read(drug_id) is None:
            raise KeyError(
                "There isn't any drug with {0} id".format(
                    drug_id))
        if self.client_card_repository.read(client_card_id) is None:
            raise KeyError(
                "There isn't any client card with {0} id".format(
                    client_card_id))

        self.transaction_repository.create(transaction)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.transaction_repository, transaction)
        self.undo_redo_service.add_to_undo(add_operation)

    def get_all(self) -> List[Transaction]:
        return self.transaction_repository.read()

    def update_transaction(self, id_transaction: str, drug_id: str,
                           client_card_id: str,
                           number_of_pieces: int,
                           date_and_hour: str) -> None:
        """
        Update transaction
        :param id_transaction: id od transaction you want to update
        :param drug_id: new drug id
        :param client_card_id: new client card id
        :param number_of_pieces: new number of pieces
        :param date_and_hour: new date and hour
        :return:
        """

        transaction = Transaction(id_transaction, drug_id,
                                  client_card_id,
                                  number_of_pieces,
                                  date_and_hour)
        if self.transaction_repository.read(id_transaction) is None:
            msg = f"There isn't any transaction with " \
                  f"{id_transaction} id."
            raise KeyError(msg)
        else:
            before_update_transaction = self.transaction_repository.read(
                id_transaction)
        self.transaction_repository.update(transaction)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.transaction_repository,
                                           before_update_transaction,
                                           transaction)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_transaction(self, transaction_id: str) -> None:
        """
        Delete transaction with transaction_id
        :param transaction_id: id transaction
        :return:
        """
        transaction_to_delete = self.transaction_repository.read(
            transaction_id)

        self.transaction_repository.delete(transaction_id)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.transaction_repository,
                                           transaction_to_delete)
        self.undo_redo_service.add_to_undo(delete_operation)

    def transaction_interval(self, start_date, end_date) -> List[Transaction]:
        """
        Creates a list with Transactions within an interval
        :param start_date: starting date
        :param end_date: ending date
        :return: a list with Transaction within starting date and ending date
        """
        result = []
        date_format = "%d-%m-%Y"
        try:

            datetime.datetime.strptime(start_date, date_format)
            datetime.datetime.strptime(end_date, date_format)
        except ValueError:
            raise ValueError("Date time format is invalid. ")
        formatted_date1 = time.strptime(start_date, "%d-%m-%Y")
        formatted_date2 = time.strptime(end_date, "%d-%m-%Y")
        for transaction in self.transaction_repository.read():
            formatted_date3 = time.strptime(
                transaction.date_and_hour.split(' ')[0], "%d-%m-%Y")
            if formatted_date1 <= formatted_date3 <= formatted_date2:
                result.append(transaction)
        return result

    def delete_transaction_interval(self, start_date, end_date) -> None:
        """
        Deletes all transaction within interval
        :param start_date: starting date of the interval
        :param end_date: ending date of the interval
        :return:
        """
        deleted_transactions = []
        try:
            date_format = "%d-%m-%Y"
            datetime.datetime.strptime(start_date, date_format)
            datetime.datetime.strptime(end_date, date_format)
        except ValueError:
            raise ValueError("Date time format is invalid. ")
        formatted_date1 = time.strptime(start_date, "%d-%m-%Y")
        formatted_date2 = time.strptime(end_date, "%d-%m-%Y")
        for transaction in self.transaction_repository.read():
            formatted_date3 = time.strptime(
                transaction.date_and_hour.split(' ')[0], "%d-%m-%Y")
            if formatted_date1 <= formatted_date3 <= formatted_date2:
                deleted_transactions.append(transaction)
                self.transaction_repository.delete(transaction.id_entity)
        self.undo_redo_service.clear_redo()
        delete_operation = DeleteIntervalOperation(self.transaction_repository,
                                                   deleted_transactions)
        self.undo_redo_service.add_to_undo(delete_operation)

    def descending_drugs(self):
        """
        :return: A list of with Drugs with their name and numbers of sales
        """
        # dictionary = {}
        # for drug in self.drug_repository.read():
        #     nr_drugs = 0
        #     for transaction in self.transaction_repository.read():
        #         if transaction.id_entity == drug.id_entity:
        #             nr_drugs = nr_drugs + 1
        #     dictionary[drug.id_entity] = nr_drugs
        # sortat = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        # for key, value in sortat:
        #     print(self.drug_repository.read(key))
        #
        drugs = self.drug_repository.read()
        transactions = self.transaction_repository.read()

        def get_number(id_drug, lst_transactions, nr_drug):
            for transaction in lst_transactions:
                if transaction.drug_id == id_drug:
                    nr_drug = nr_drug + 1
            return nr_drug

        def inner(lst_drugs, lst_transactions):
            if not lst_drugs:
                return []
            medicine = lst_drugs[0]
            number_of_drugs = 0
            for transaction in lst_transactions:
                if medicine.id_entity == transaction.drug_id:
                    number_of_drugs = get_number(medicine.id_entity,
                                                 lst_transactions,
                                                 int(0))
            return [DrugsNoSales(medicine.drug_name, number_of_drugs)] + inner(
                lst_drugs[1:], lst_transactions)

        lst_no_sale = inner(drugs, transactions)
        # return sorted(lst_no_sale, key=lambda x: x.number_of_sales,
        #               reverse=True)
        return my_sorted(lst_no_sale, key=lambda x: x.number_of_sales,
                         reverse=True)

    def descending_sales(self) -> None:
        dictionary = {}
        for client in self.client_card_repository.read():
            nr_discount = 0
            for transaction in self.transaction_repository.read():
                if client.id_entity == transaction.id_entity:
                    if float(self.transaction_sale(client.id_entity,
                                                   transaction.drug_id)[
                                 1]) >= 0:
                        nr_discount += 1
                    dictionary[client.id_entity] = nr_discount
                    sortat = sorted(dictionary.items(), key=lambda x: x[1],
                                    reverse=True)
                    for key, value in sortat:
                        print(self.client_card_repository.read(key))

    def transaction_sale(self, id_client_card=None, id_drug=None) \
            -> Union[List[Union[float, str]], str]:
        """
        Apply the sale for people who have a client card
        :param id_client_card: id client card
        :param id_drug: id drug
        :return: if the client has a card returns a tuple with new_price,
        the discount applied,if not returns a tuple with the price without
        discount and -1
        """
        client_card_repo = self.client_card_repository.read()
        drug_repo = self.drug_repository.read()
        if id_client_card is not None:
            for id_card in client_card_repo:
                if id_card.id_entity == id_client_card:
                    for drug in drug_repo:
                        if drug.id_entity == id_drug:
                            if drug.need_recipe == 'Yes':
                                return [drug.drug_price - (
                                        (15 * drug.drug_price) / 100), '15']
                            else:
                                return [drug.drug_price - (
                                        (10 * drug.drug_price) / 100), '10']
        if id_client_card == '':
            for drug in drug_repo:
                if drug.id_entity == id_drug:
                    return [drug.drug_price, '-1']
