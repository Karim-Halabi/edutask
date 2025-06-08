import json
from src.util import validators
import pytest
import os
from pymongo import MongoClient, errors
from src.util.dao import DAO

def load_test_validator(collection_name: str):
    test_path = os.path.join(os.path.dirname(__file__), "validators", f"{collection_name}.json")
    with open(test_path, "r") as f:
        return json.load(f)

validators.getValidator = load_test_validator

@pytest.fixture(scope="module")
def test_db():
    client = MongoClient('mongodb://localhost:27017')
    db = client['edutask']
    collection_name = 'test_collection'

    if collection_name in db.list_collection_names():
        db.drop_collection(collection_name)

    dao = DAO(collection_name=collection_name)

    yield dao

    db.drop_collection(collection_name)
    client.close()

def test_create_valid_document(test_db):
    valid_document = {
        "name": "Karim Halabi", 
        "age": 21}
    result = test_db.create(valid_document)
    assert result is not None
    assert result["name"] == "Karim Halabi"

def test_create_invalid_document_missing_field(test_db):
    invalid_document = {"age": 21}  
    with pytest.raises(errors.WriteError):
        test_db.create(invalid_document)

def test_create_invalid_document_wrong_type(test_db):
    invalid_document = {"name": 12345, 
                        "age": "twenty one"}  
    with pytest.raises(errors.WriteError):
        test_db.create(invalid_document)

def test_create_mongo_unavailable(monkeypatch):
    from pymongo.errors import ConnectionFailure
    from src.util.dao import DAO

    def mock_create_fail(*args, **kwargs):
        raise ConnectionFailure("Mock DB Connection Error")

    dao = DAO(collection_name='test_collection')
    monkeypatch.setattr(dao, 'create', mock_create_fail)

    with pytest.raises(ConnectionFailure):
        dao.create({"name": "Karim"})
