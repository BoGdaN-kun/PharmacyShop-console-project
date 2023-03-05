import random
import string

from Domain import DrugValidation
from Domain.Drug import Drug
from Domain.genrand_undo_redo import GenerateAddUndoRedo
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class GenerateEntityService:
    def __init__(self, drug_repository: Repository,
                 drug_validator: DrugValidation,
                 undo_redo_service: UndoRedoService):
        self.drug_repository = drug_repository
        self.drug_validator = drug_validator
        self.undo_redo_service = undo_redo_service

    def generate(self, n: int):
        """
        Generates n entities
        :param n: number of entities you want to generate
        :return:
        """
        before_generate = []
        for i in range(0, n):
            id_drug = str(random.randint(200, 100000000) + i)

            drug_name = ''.join(random.choices(string.ascii_lowercase,
                                               k=random.randint(5, 10)))
            drug_producer = ''.join(random.choices(string.ascii_lowercase,
                                                   k=random.randint(5, 10)))
            drug_price = random.randint(1, 9000)
            need_recipe = random.choice(['Yes', 'No'])
            drug = Drug(id_drug, drug_name, drug_producer, drug_price,
                        need_recipe)

            try:
                # Validate the drug
                self.drug_validator.validate(drug)
                self.drug_repository.create(drug)
                before_generate.append(drug)
            except ValueError:
                # If the id is already in the repository we will try again with a new id until
                # we find one that is not in the repository yet
                if i != 0:
                    i -= 1
                else:
                    i = 0
        self.undo_redo_service.clear_redo()
        add_operation = GenerateAddUndoRedo(self.drug_repository,
                                            before_generate)
        self.undo_redo_service.add_to_undo(add_operation)
