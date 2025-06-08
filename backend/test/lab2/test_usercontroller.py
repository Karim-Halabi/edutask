import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def mock_dao():
    return MagicMock(spec=DAO)

@pytest.fixture
def user_controller(mock_dao):
    return UserController(dao=mock_dao)

def test_tc1_valid_email(user_controller, mock_dao):
    user = {'email': 'test1@test.com', 'name': 'User One'}
    mock_dao.find.return_value = [user]
    result = user_controller.get_user_by_email('test1@test.com')
    assert result == user

def test_tc2a_returns_first_user(user_controller, mock_dao):
    users = [{'email': 'test2@test.com'}, {'email': 'test2@test.com'}]
    mock_dao.find.return_value = users
    result = user_controller.get_user_by_email('test2@test.com')
    assert result == users[0]

def test_tc2b_logs_warning(user_controller, mock_dao, capsys):
    users = [{'email': 'test2@test.com'}, {'email': 'test2@test.com'}]
    mock_dao.find.return_value = users
    user_controller.get_user_by_email('test2@test.com')
    captured = capsys.readouterr()
    assert "more than one user found" in captured.out


def test_tc3_none(user_controller, mock_dao):
    mock_dao.find.return_value = []
    result = user_controller.get_user_by_email('test3@test.com')
    assert result is None

# Missing @
def test_tc4_invalid(user_controller):
    with pytest.raises(ValueError, match="invalid email address"):
        user_controller.get_user_by_email('test4.gmail.com')

# Missing dot
def test_tc5_invalid(user_controller):
    with pytest.raises(ValueError, match="invalid email address"):
        user_controller.get_user_by_email('test5@testcom')

# Two @
def test_tc6_invalid(user_controller):
    with pytest.raises(ValueError, match="invalid email address"):
        user_controller.get_user_by_email('test6@@test.com')
# Empty email
def test_tc7_invalid(user_controller):
    with pytest.raises(ValueError, match="invalid email address"):
        user_controller.get_user_by_email("")

def test_tc8_exception(user_controller, mock_dao):
    mock_dao.find.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        user_controller.get_user_by_email('test8@test.com')
