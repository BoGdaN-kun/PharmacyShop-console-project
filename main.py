from Domain.ClientCardValidation import ClientCardValidation
from Domain.DrugValidation import DrugValidator
from Domain.TransactionValidation import TransactionValidation
from Repository.JsonRepository import RepositoryJson
from Service.ClientCardService import ClientCardService
from Service.DrugService import DrugService
from Service.RandomEntityGenerator import GenerateEntityService
from Service.TransactionService import TransactionService
from Service.cascade_deletionservice import CascadeDeletion
from Service.undo_redo_service import UndoRedoService
from Tests.ALL_TESTS import all_tests
from UserInterface.Console import Console


def main():
    undo_redo_service = UndoRedoService()

    drug_repository = RepositoryJson('drugs.json')
    drug_validator = DrugValidator()
    drug_service = DrugService(drug_repository, drug_validator,
                               undo_redo_service)
    generator_service = GenerateEntityService(drug_repository, drug_validator,
                                              undo_redo_service)
    client_card_repository = RepositoryJson('client_cards.json')
    client_card_validator = ClientCardValidation()
    client_card_service = ClientCardService(client_card_repository,
                                            client_card_validator,
                                            undo_redo_service)

    transaction_repository = RepositoryJson('transactions.json')
    transaction_validator = TransactionValidation()
    transaction_service = TransactionService(transaction_repository,
                                             drug_repository,
                                             client_card_repository,
                                             transaction_validator,
                                             undo_redo_service)
    cascade_deletion_service = CascadeDeletion(drug_repository,
                                               client_card_repository,
                                               transaction_repository,
                                               drug_service,
                                               transaction_service,
                                               client_card_service,
                                               undo_redo_service)

    # transaction_service.add_transaction('12899889', '15149195', '12', 222,
    #                                     '11-11-1111 11:11')
    # transaction_service.add_transaction('12289889', '15149195', '12', 222,
    #                                     '11-11-1111 11:11')

    console = Console(drug_service, client_card_service, transaction_service,
                      generator_service, cascade_deletion_service,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    all_tests()
    main()
