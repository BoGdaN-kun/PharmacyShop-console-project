from typing import List

from Domain import DrugValidation
from Domain.Drug import Drug
from Domain.Undo_redo_increase import IncrementOperation
from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class DrugService:
    def __init__(self, drug_repository: Repository,
                 drug_validator: DrugValidation,
                 undo_redo_service: UndoRedoService):
        self.drug_repository = drug_repository
        self.drug_validator = drug_validator
        self.undo_redo_service = undo_redo_service

    def add_drug(self, id_drug, drug_name,
                 drug_producer, drug_price,
                 need_recipe) -> None:
        """
        Adds a drug
        :param id_drug:id_drug
        :param drug_name:drug_name
        :param drug_producer:drug_producer
        :param drug_price:drug_price
        :param need_recipe:need_recipe
        :return:
        """
        drug = Drug(id_drug, drug_name,
                    drug_producer, drug_price,
                    need_recipe)
        self.drug_validator.validate(drug)
        if self.drug_repository.read(id_drug) is not None:
            raise KeyError("There is already a drug with"
                           " the id {0}".format(id_drug))

        self.drug_repository.create(drug)
        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.drug_repository, drug)
        self.undo_redo_service.add_to_undo(add_operation)

    def get_all(self) -> List[Drug]:
        return self.drug_repository.read()

    def update_drug(self, id_drug: str, drug_name: str,
                    drug_producer: str,
                    drug_price: float, need_recipe: str) -> None:
        """
        Update a drug with id
        :param id_drug:new id drug
        :param drug_name:new drug name
        :param drug_producer:new drug producer
        :param drug_price:new drug price
        :param need_recipe:new need recipe
        :return:
        """
        drug = Drug(id_drug, drug_name,
                    drug_producer,
                    drug_price,
                    need_recipe)
        if self.drug_repository.read(id_drug) is None:
            msg = f"There isn't any drug with {id_drug} id."
            raise KeyError(msg)
        else:
            before_update_drug = self.drug_repository.read(
                id_drug)

        self.drug_validator.validate(drug)
        self.drug_repository.update(drug)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.drug_repository,
                                           before_update_drug, drug)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_drug(self, id_drug: str) -> None:
        """
        Deletes the drug with id_drug
        :param id_drug: id drug
        :return:
        """
        drug_to_delete = self.drug_repository.read(
            id_drug)

        self.drug_repository.delete(id_drug)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.drug_repository,
                                           drug_to_delete)
        self.undo_redo_service.add_to_undo(delete_operation)

    def increase_price(self, value: float, percentile: float) -> None:
        """
        Increase price for drugs
        :param value: value
        :param percentile: increase with %
        :return:
        """
        before_increase = []
        after_increase = []
        for drug in self.drug_repository.read():
            if drug.drug_price < value:
                new_price = drug.drug_price + (
                        drug.drug_price * percentile) / 100
                before_increase.append(drug)
                self.update_drug(drug.id_entity, drug.drug_name,
                                 drug.drug_producer, new_price,
                                 drug.need_recipe)
        for drug in self.drug_repository.read():
            after_increase.append(drug)
        self.undo_redo_service.clear_redo()
        increment_operation = IncrementOperation(self.drug_repository,
                                                 before_increase,
                                                 after_increase)
        self.undo_redo_service.add_to_undo(increment_operation)

    def search(self, text) -> List:
        """
        Returns a list with Drug Objects where text is in
        :param text: text you want to search
        :return:
        """
        result = []
        drugs = self.drug_repository.read()
        if check_float(text) is False:
            for drug in drugs:
                if (text in drug.drug_name) or (text in drug.id_entity) or (
                        text in drug.need_recipe) or (
                        text in drug.drug_producer):
                    result.append(drug)
            return result
        else:
            for drug in drugs:
                if str(text) in str(drug.drug_price):
                    result.append(drug)
            return result


def check_float(number: float):
    """
    It checks if the number is float
    :param number: number to check
    :return: True if is float,False if not
    """
    try:
        float(number)
        return True
    except ValueError:
        return False
