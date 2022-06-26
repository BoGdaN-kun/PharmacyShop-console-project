from Domain.ClientCard import ClientCard
from Domain.ClientCardValidation import ClientCardValidation
from Repository.JsonRepository import RepositoryJson
from Service.ClientCardService import ClientCardService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_client_card_service():
    filename = 'test_client_card_service.json'
    clear_file(filename)
    client_card_repository = RepositoryJson(filename)
    undo_redo_service = UndoRedoService()
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
    assert client_card_repository.read(added.id_entity) == added
    client_card_service.add_client_card('14', 'PPP', 'Op', '1234123412345',
                                        '11-11-1111',
                                        '11-11-1111')
    client_card_service.delete_client_card('12')
    assert client_card_repository.read('12') is None
    before_update = client_card_repository.read()
    client_card_service.update_client_card('13', 'Uuu', 'Op', '1234551234551',
                                           '11-11-1111',
                                           '11-11-1111')
    assert before_update != client_card_repository.read()
