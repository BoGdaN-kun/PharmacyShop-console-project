from Domain.ClientCard import ClientCard
from Domain.ClientCardValidation import ClientCardValidation
from Repository.JsonRepository import RepositoryJson
from Service.ClientCardService import ClientCardService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def full_search_client_cards():
    filename = 'test_client_cards.json'
    clear_file(filename)
    client_repository = RepositoryJson(filename)
    client_cards_validator = ClientCardValidation()
    undo_redo_service = UndoRedoService()
    client_cards_service = ClientCardService(client_repository,
                                             client_cards_validator,
                                             undo_redo_service)
    added = ClientCard('12', 'Tom', 'Holland', '12345', '11-11-1111',
                       '11-11-1111')
    client_repository.create(added)
    text = 'To'
    searched = client_cards_service.search(text)
    assert searched is not None
    assert searched[0] == added
