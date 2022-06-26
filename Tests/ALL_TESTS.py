from Tests.TestClientCardRepository import test_client_card_repository
from Tests.TestClientCardService import test_client_card_service
from Tests.TestDrugRepository import test_drug_repository
from Tests.TestDrugService import test_drug_service
from Tests.TestTransaction import test_transaction
from Tests.TestTransactionService import test_transaction_service
from Tests.cascade_test import cascade_test
from Tests.cascade_undo_redo import cascade_undo_redo_test
from Tests.fullsearch_clientcards import full_search_client_cards
from Tests.fulltextsearch_drugs import full_search_drugs
from Tests.genrand_undo_redo_test import test_generate_undo_random_entity
from Tests.test_genrand import test_generate_random_entity


def all_tests():
    test_client_card_repository()
    test_client_card_service()
    test_drug_repository()
    test_drug_service()
    test_transaction()
    test_transaction_service()
    full_search_drugs()
    full_search_client_cards()
    test_generate_random_entity()
    cascade_test()
    test_generate_undo_random_entity()
    cascade_undo_redo_test()
