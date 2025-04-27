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

def test_single_user_found(user_controller, mock_dao):
    user = {'email': 'karim@gamil.com', 'name': 'Karim'}
    mock_dao.find.return_value = [user]
    result = user_controller.get_user_by_email('karim@gmail.com')
    assert result == user

def test_multiple_users_found(user_controller, mock_dao, capsys):
    users = [{'email': 'karim@gmail.com'}, {'email': 'karim@gmail.com'}]
    mock_dao.find.return_value = users
    result = user_controller.get_user_by_email('karim@gamil.com')
    captured = capsys.readouterr()
    assert "more than one user found" in captured.out
    assert result == users[0]

def test_no_users_found(user_controller, mock_dao):
    mock_dao.find.return_value = []
    result = user_controller.get_user_by_email('karim@gamil.com')
    assert result is None

def test_invalid_email(user_controller):
    with pytest.raises(ValueError, match="invalid email address"):
        user_controller.get_user_by_email('karim.com')

def test_dao_exception(user_controller, mock_dao):
    mock_dao.find.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        user_controller.get_user_by_email('karim@gmail.com')
