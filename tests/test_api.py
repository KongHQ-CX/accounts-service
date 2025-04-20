"""
Test fixtures for the Accounts service tests.
"""

import pytest
from fastapi.testclient import TestClient

from accounts.main import app
from accounts.services.account import AccountService, account_service


@pytest.fixture
def client():
    """Test client fixture for API tests"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_account_service():
    """Reset the account service singleton between tests"""
    account_service._accounts_db = {}
    yield
    account_service._accounts_db = {}


@pytest.fixture
def new_account_service():
    """Fixture that returns a fresh instance of the account service"""
    return AccountService()
