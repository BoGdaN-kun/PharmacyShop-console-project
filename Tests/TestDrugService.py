from Domain.Drug import Drug
from Domain.DrugValidation import DrugValidator
from Repository.JsonRepository import RepositoryJson
from Service.DrugService import DrugService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_drug_service():
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
    assert drug_repository.read(added.id_entity) == added
    drug_service.add_drug('13', 'Oal', 'Hey', 133233, 'No')
    drug_service.delete_drug('12')
    assert len(drug_repository.read()) == 2
    before_update = drug_repository.read()
    drug_service.update_drug('14', 'Haha', 'Cola', 1222, 'Yes')
    assert before_update != drug_repository.read()

    drug_service.increase_price(200, 10)
    assert drug_repository.read('14') == Drug('14', 'Haha', 'Cola', 1222,
                                              'Yes')
    added = Drug('12', 'Paracetamol', 'Teddy', 123.0, 'Yes')
    drug_repository.create(added)
    drug_service.increase_price(200, 10)
    assert drug_repository.read('12') == Drug('12', 'Paracetamol', 'Teddy',
                                              135.3, 'Yes')
