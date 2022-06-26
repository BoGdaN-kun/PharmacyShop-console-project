from Domain.ClientCard import ClientCard
from Domain.ClientCardValidation import ClientCardValidation
from Domain.Drug import Drug
from Domain.DrugValidation import DrugValidator
from Domain.TransactionValidation import TransactionValidation
from Repository.JsonRepository import RepositoryJson
from Service.ClientCardService import ClientCardService
from Service.DrugService import DrugService
from Service.TransactionService import TransactionService
from Service.cascade_deletionservice import CascadeDeletion
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def cascade_undo_redo_test():
    undo_redo_service = UndoRedoService()
    filename_1 = 'test_drugs_service.json'
    filename_2 = 'test_client_card_service.json'
    filename_3 = 'test_transaction_service.json'
    clear_file(filename_1)
    clear_file(filename_2)
    clear_file(filename_3)
    client_card_repository = RepositoryJson(filename_2)
    drug_repository = RepositoryJson(filename_1)
    transactions_repository = RepositoryJson(filename_3)
    added = Drug('12', 'Paracetamol', 'Teddy', 123.0, 'Yes')
    drug_validator = DrugValidator()
    undo_redo_service = UndoRedoService()
    drug_service = DrugService(drug_repository, drug_validator,
                               undo_redo_service)
    drug_service.add_drug('14', 'Pal', 'Hey', 1233, 'Yes')
    drug_repository.create(added)
    added = ClientCard('12', 'Hala', 'Halo', '1234123412341', '11-11-1111',
                       '11-11-1111')
    client_card_validation = ClientCardValidation()
    client_card_service = ClientCardService(client_card_repository,
                                            client_card_validation,
                                            undo_redo_service)
    client_card_service.add_client_card('13', 'Uuu', 'Op', '1234123412341',
                                        '11-11-1111',
                                        '11-11-1111')
    client_card_repository.create(added)
    transaction_validation = TransactionValidation()
    transaction_service = TransactionService(transactions_repository,
                                             drug_repository,
                                             client_card_repository,
                                             transaction_validation,
                                             undo_redo_service)
    transaction_service.add_transaction('12', '12', '12', 222,
                                        '11-11-1111 11:11')
    before_cascade_drug = drug_repository.read()
    before_cascade_trans = transactions_repository.read()
    before_cascade_client = client_card_repository.read()
    cascade_deletion = CascadeDeletion(drug_repository, client_card_repository,
                                       transactions_repository, drug_service,
                                       transaction_service,
                                       client_card_service, undo_redo_service)
    drug_service.add_drug('15', 'Pal', 'Hey', 1233, 'Yes')
    after_cascade_drug = drug_repository.read()
    after_cascade_trans = transactions_repository.read()
    after_cascade_client = client_card_repository.read()
    undo_redo_service.do_undo()
    assert len(before_cascade_client) == len(client_card_repository.read())
    assert len(before_cascade_trans) == len(transactions_repository.read())
    assert len(before_cascade_drug) == len(drug_repository.read())
    undo_redo_service.do_redo()
    assert len(after_cascade_client) == len(client_card_repository.read())
    assert len(after_cascade_trans) == len(transactions_repository.read())
    assert len(after_cascade_drug) == len(drug_repository.read())
    try:
        assert drug_repository.read('14') is not None
        cascade_deletion.delete('14', 'drug')
        assert drug_repository.read('14') is None
        assert client_card_repository.read('13') is not None
        cascade_deletion.delete('13', 'client card')
        assert drug_repository.read('13') is None

    except ValueError:
        pass
