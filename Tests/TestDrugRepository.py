from Domain.Drug import Drug
from Repository.JsonRepository import RepositoryJson
from Repository.exceptions import NoSuchIdError, DuplicateIdError
from utils import clear_file


def test_drug_repository():
    filename = 'test_drugs.json'
    clear_file(filename)
    drug_repository = RepositoryJson(filename)
    added = Drug('12', 'Paracetamol', 'Teddy', 123.0, 'Yes')
    try:
        drug_repository.create(added)
        assert drug_repository.read(added.id_entity) == added
        drug_repository.create(added)
        assert drug_repository.read(added.id_entity) == added
    except DuplicateIdError:
        pass
    drug_repository.delete(added.id_entity)

    assert drug_repository.read(added.id_entity) is None
    try:
        assert drug_repository.update(added)
    except NoSuchIdError:
        pass
