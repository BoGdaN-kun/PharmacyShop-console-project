from Domain.Drug import Drug
from Domain.DrugValidation import DrugValidator
from Repository.JsonRepository import RepositoryJson
from Service.DrugService import DrugService
from Service.RandomEntityGenerator import GenerateEntityService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_generate_undo_random_entity():
    filename = 'test_drugs_service.json'
    clear_file(filename)
    drug_repository = RepositoryJson(filename)
    added = Drug('12', 'Paracetamol', 'Teddy', 123.0, 'Yes')
    drug_validator = DrugValidator()
    undo_redo_service = UndoRedoService()
    drug_service = DrugService(drug_repository, drug_validator,
                               undo_redo_service)
    drug_service.add_drug('14', 'Pal', 'Hey', 1233, 'Yes')
    drug_repository.create(added)
    generate_entity_service = GenerateEntityService(drug_repository,
                                                    drug_validator,
                                                    undo_redo_service)
    before_length = len(drug_repository.read())
    before_generate = drug_repository.read()
    generate_entity_service.generate(3)
    length = len(drug_repository.read())
    assert before_length + 3 == length
    after_generate = drug_repository.read()
    undo_redo_service.do_undo()

    assert len(before_generate) == len(drug_repository.read())
    undo_redo_service.do_redo()
    assert len(after_generate) == len(drug_repository.read())
