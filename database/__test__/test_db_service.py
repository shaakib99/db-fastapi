from unittest.mock import patch
from database.service import DatabaseService
from demo.schemas import DemoUser
import pytest

@pytest.fixture
def user():
    yield DemoUser(id = 1, name = 'test', email = 'test@email.com')


@patch('database.service.MySQLDatabase')
def test_db_service(mysql_database, user):
    user_service = DatabaseService(DemoUser, mysql_database)

    user_service.service.connect.return_value =  lambda: True
    user_service.service.disconnect.return_value = True
    user_service.service.create_metadata.return_value = True
    user_service.service.getOneById.return_value =  user
    user_service.service.saveOne.return_value = user
    user_service.service.updateOne.return_value = user
    user_service.service.deleteOne.return_value = True
    user_service.service.getAll.return_value = [user]


    assert user_service.connect() is None, "Must connect to the database"
    assert user_service.disconnect() is None, "Must disconnect to the database"
    assert user_service.create_metadata() is None, "Must create metadata in the database"
    assert user_service.getOne(1) == user, "GetOne must be functional"
    assert user_service.saveOne({}) == user, "SaveOne must be functional"
    assert user_service.deleteOne(1) is True, "DeleteOne must be functional"
    assert user_service.updateOne(1, {}) == user, "UpdateOne must be functional"
    assert len(user_service.getAll({})) == 1, "getAll should return list"





