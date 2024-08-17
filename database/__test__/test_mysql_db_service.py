from database.mysql_db_service import MySQLDatabase
from demo.schemas import DemoUser
from demo.models import DemoUserModel, DemoResponseUserModel
from database.models.query_param_model import SQLQueryParam
import pytest

@pytest.fixture()
def database():
    mysql_db_service = MySQLDatabase.get_instance()
    mysql_db_service.create_metadata()

    yield mysql_db_service

    mysql_db_service.drop_metadata()
    mysql_db_service.disconnect()

@pytest.fixture
def user_data():
    demo_user = DemoUserModel(name = 'wahid', email = 'test@email.com')
    yield demo_user




def test_connect(database):
    database.connect()

def test_disconnect(database):
    database.disconnect()

def test_same_instance():
    mysql_db_service1 = MySQLDatabase.get_instance()
    mysql_db_service2 = MySQLDatabase.get_instance()

    assert mysql_db_service1 == mysql_db_service2, 'MySQLDatabase.get_instance is not returing same instance'

def test_create_metadata():
    mysql_db_service = MySQLDatabase.get_instance()
    mysql_db_service.create_metadata()

def test_get_one_by_id(database, user_data):
    result = database.saveOne(DemoUser, user_data.model_dump())

    assert result.id is not None, 'User should exist'

    assert database.getOneById(DemoUser, result.id) is not None, 'User should exist'

def test_update_one_by_id(database, user_data):
    result = database.saveOne(DemoUser, user_data.model_dump())

    assert result.id is not None, 'User should exist'

    result = database.updateOne(DemoUser, result.id, {'name': 'wahid_update'})

    assert result.name == 'wahid_update', 'User data should update'

def test_delete_one_by_id(database, user_data):
    result = database.saveOne(DemoUser, user_data.model_dump())

    assert result.id is not None, 'User should exist'

    user_id = result.id

    result = database.deleteOne(DemoUser, result.id)

    assert database.getOneById(DemoUser, user_id) is None, 'Deleted User should not exist'

def test_get_all(database, user_data):
    database.saveOne(DemoUser, user_data.model_dump())
    user_data.email = 'test2@email.com'
    database.saveOne(DemoUser, user_data.model_dump())

    result = database.getAll(DemoUser, SQLQueryParam(selected_fields = [], join = []))

    assert len(result) == 2, 'There should be only 2 result'
    assert result[1].email == user_data.email, f'Email should {user_data.email}'

    result = database.getAll(DemoUser, SQLQueryParam(limit = 1, selected_fields = [], join = []))

    assert len(result) == 1, 'There should be only 1 result after use limit'

    result = database.getAll(DemoUser, SQLQueryParam(selected_fields = ['id', 'name'], join = []))

    result = DemoResponseUserModel.model_validate(result[1])
    assert getattr(result, 'email') is None, "Only Id and name field should return"

    result = database.getAll(DemoUser, SQLQueryParam(selected_fields = ['id'], join = ['licenses']))
    result = DemoResponseUserModel.model_validate(result[1])


    # result = DemoResponseUserModel.model_validate(result[1])
    assert len(getattr(result, 'licenses')) == 0, "licenses field should return when joining"






