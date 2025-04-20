"""
Tests for the Account Service logic.
"""

import uuid
from uuid import UUID

import pytest

from accounts.api.models import AccountType
from accounts.services.account import AccountService


@pytest.fixture
def account_service():
    """Create a fresh account service for testing"""
    return AccountService()


def test_create_account(account_service):
    """Test creating a new account"""
    # Create a checking account
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=1000.0
    )

    # Verify account properties
    assert account.type == AccountType.CHECKING
    assert account.balance == 1000.0
    assert isinstance(account.account_id, UUID)


def test_create_account_with_zero_balance(account_service):
    """Test creating a new account with zero balance"""
    account = account_service.create_account(
        account_type=AccountType.SAVINGS, initial_balance=0.0
    )

    assert account.balance == 0.0


def test_create_account_with_negative_balance(account_service):
    """Test creating a new account with negative balance raises error"""
    with pytest.raises(ValueError) as excinfo:
        account_service.create_account(
            account_type=AccountType.CHECKING, initial_balance=-100.0
        )

    assert "non-negative" in str(excinfo.value)


def test_get_account(account_service):
    """Test retrieving an account by ID"""
    # Create an account first
    created_account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=1500.0
    )

    # Get the account by ID
    retrieved_account = account_service.get_account(created_account.account_id)

    # Verify it's the same account
    assert retrieved_account.account_id == created_account.account_id
    assert retrieved_account.type == AccountType.CHECKING
    assert retrieved_account.balance == 1500.0


def test_get_nonexistent_account(account_service):
    """Test retrieving a non-existent account returns None"""
    random_id = uuid.uuid4()
    account = account_service.get_account(random_id)
    assert account is None


def test_list_accounts(account_service):
    """Test listing all accounts"""
    # Initially should be empty
    accounts = account_service.list_accounts()
    assert len(accounts) == 0

    # Create a couple of accounts
    account_service.create_account(AccountType.CHECKING, 1000.0)
    account_service.create_account(AccountType.SAVINGS, 2000.0)

    # List should now contain 2 accounts
    accounts = account_service.list_accounts()
    assert len(accounts) == 2


def test_credit_account(account_service):
    """Test crediting an account"""
    # Create an account first
    account = account_service.create_account(
        account_type=AccountType.SAVINGS, initial_balance=500.0
    )

    # Credit the account
    updated_account = account_service.credit_account(
        account_id=account.account_id, amount=250.0
    )

    # Verify the balance increased
    assert updated_account.balance == 750.0

    # Verify the account in the service was updated
    stored_account = account_service.get_account(account.account_id)
    assert stored_account.balance == 750.0


def test_credit_nonexistent_account(account_service):
    """Test crediting a non-existent account raises KeyError"""
    random_id = uuid.uuid4()

    with pytest.raises(KeyError) as excinfo:
        account_service.credit_account(random_id, 100.0)

    assert "not found" in str(excinfo.value)


def test_credit_zero_amount(account_service):
    """Test crediting with zero amount raises ValueError"""
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=100.0
    )

    with pytest.raises(ValueError) as excinfo:
        account_service.credit_account(account.account_id, 0.0)

    assert "positive" in str(excinfo.value)


def test_credit_negative_amount(account_service):
    """Test crediting with negative amount raises ValueError"""
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=100.0
    )

    with pytest.raises(ValueError) as excinfo:
        account_service.credit_account(account.account_id, -50.0)

    assert "positive" in str(excinfo.value)


def test_debit_account(account_service):
    """Test debiting an account"""
    # Create an account first
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=1000.0
    )

    # Debit the account
    updated_account = account_service.debit_account(
        account_id=account.account_id, amount=300.0
    )

    # Verify the balance decreased
    assert updated_account.balance == 700.0

    # Verify the account in the service was updated
    stored_account = account_service.get_account(account.account_id)
    assert stored_account.balance == 700.0


def test_debit_insufficient_funds(account_service):
    """Test debiting more than the account balance raises ValueError"""
    account = account_service.create_account(
        account_type=AccountType.SAVINGS, initial_balance=100.0
    )

    with pytest.raises(ValueError) as excinfo:
        account_service.debit_account(account.account_id, 200.0)

    assert "Insufficient funds" in str(excinfo.value)


def test_debit_exact_balance(account_service):
    """Test debiting the exact account balance works"""
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=100.0
    )

    updated_account = account_service.debit_account(account.account_id, 100.0)
    assert updated_account.balance == 0.0


def test_debit_nonexistent_account(account_service):
    """Test debiting a non-existent account raises KeyError"""
    random_id = uuid.uuid4()

    with pytest.raises(KeyError) as excinfo:
        account_service.debit_account(random_id, 100.0)

    assert "not found" in str(excinfo.value)


def test_debit_zero_amount(account_service):
    """Test debiting with zero amount raises ValueError"""
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=100.0
    )

    with pytest.raises(ValueError) as excinfo:
        account_service.debit_account(account.account_id, 0.0)

    assert "positive" in str(excinfo.value)


def test_debit_negative_amount(account_service):
    """Test debiting with negative amount raises ValueError"""
    account = account_service.create_account(
        account_type=AccountType.CHECKING, initial_balance=100.0
    )

    with pytest.raises(ValueError) as excinfo:
        account_service.debit_account(account.account_id, -50.0)

    assert "positive" in str(excinfo.value)
