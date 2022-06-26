from Domain.Transaction import Transaction
from Repository.JsonRepository import RepositoryJson
from Repository.exceptions import DuplicateIdError, NoSuchIdError
from utils import clear_file


def test_transaction():
    filename = 'test_transactions.json'
    clear_file(filename)
    transaction_repository = RepositoryJson(filename)
    added = Transaction('12', '123', '122',
                        22, '11-11-2021 11:10')
    transaction_repository.create(added)
    try:
        assert transaction_repository.read(added.id_entity) == added

    except DuplicateIdError:
        pass
    transaction_repository.delete(added.id_entity)

    assert transaction_repository.read(added.id_entity) is None
    try:
        assert transaction_repository.update(added)
    except NoSuchIdError:
        pass
