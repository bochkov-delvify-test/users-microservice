import pytest
from httpx import Client
from starlette.testclient import TestClient

from delvify.main import ms
from delvify.models import User


@pytest.fixture()
def client() -> Client:
    return TestClient(ms)


@pytest.fixture
def test_user() -> User:
    user = User()
    user.id = 1
    user.email = 'test@test.com'
    user.password = 'test_password'
    return user
