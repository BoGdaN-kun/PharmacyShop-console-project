from Domain.ClientCard import ClientCard
from Repository.JsonRepository import RepositoryJson
from Repository.exceptions import NoSuchIdError
from utils import clear_file


def test_client_card_repository():
    filename = 'test_client_cards.json'
    clear_file(filename)
    client_repository = RepositoryJson(filename)
    added = ClientCard('12', 'Tom', 'Holland', '12345', '11-11-1111',
                       '11-11-1111')
    client_repository.create(added)
    assert client_repository.read(added.id_entity) == added

    client_repository.delete(added.id_entity)

    assert client_repository.read(added.id_entity) is None
    try:
        assert client_repository.update(added)
    except NoSuchIdError:
        pass
