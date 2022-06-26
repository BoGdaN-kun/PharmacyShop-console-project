from Domain.ClientCard import ClientCard
from Domain.ClientCardValidation import ClientCardValidation
from Domain.Drug import Drug
from Domain.DrugValidation import DrugValidator
from Domain.Transaction import Transaction
from Domain.TransactionValidation import TransactionValidation
from Repository.JsonRepository import RepositoryJson
from Service.ClientCardService import ClientCardService
from Service.DrugService import DrugService
from Service.TransactionService import TransactionService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_transaction_service():
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
    added = Transaction('12', '12', '12', 222, '11-11-1111 11:11')
    transaction_service.add_transaction('12', '12', '12', 222,
                                        '11-11-1111 11:11')
    assert transactions_repository.read(added.id_entity) == added
    transaction_service.add_transaction('14', '12', '12', 222,
                                        '11-11-1111 11:11')
    transaction_service.delete_transaction('14')
    assert len(transactions_repository.read()) == 1
    before_update = transactions_repository.read()
    transaction_service.update_transaction('12', '12', '12', 122,
                                           '11-11-1111 11:22')
    assert before_update != transactions_repository.read()
    transaction_service.add_transaction('14', '12', '12', 222,
                                        '11-11-2020 11:11')
    transaction_service.delete_transaction_interval('10-11-1111', '20-11-1111')
    assert transactions_repository.read('12') is None
