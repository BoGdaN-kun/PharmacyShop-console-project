from Domain.Drug import Drug
from Domain.DrugValidation import DrugValidator
from Repository.JsonRepository import RepositoryJson
from Service.DrugService import DrugService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def full_search_drugs():
    filename = 'fulltextsearch_drugs.json'
    clear_file(filename)
    drug_repository = RepositoryJson(filename)
    drug_validator = DrugValidator()
    undo_redo_service = UndoRedoService()
    drug_service = DrugService(drug_repository, drug_validator,
                               undo_redo_service)
    added = Drug('12', 'Paracetamol', 'Teddy', 123.0, 'Yes')
    text = 'Para'
    drug_repository.create(added)
    searched = drug_service.search(text)
    assert searched is not None
    assert searched[0] == added
