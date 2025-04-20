"""
Account service module for business logic related to bank accounts.
"""

from typing import Dict, List, Optional
from uuid import UUID, uuid4

from accounts.api.models import Account, AccountType


class AccountService:
    """Service for handling account operations"""

    def __init__(self) -> None:
        """Initialize the account service with an empty database."""
        self._accounts_db: Dict[UUID, Account] = {}

    def list_accounts(self) -> List[Account]:
        """Returns a list of all accounts."""
        return list(self._accounts_db.values())

    def get_account(self, account_id: UUID) -> Optional[Account]:
        """Get an account by its ID."""
        return self._accounts_db.get(account_id)

    def create_account(
        self, account_type: AccountType, initial_balance: float
    ) -> Account:
        """Create a new account with the specified type and initial balance."""
        if initial_balance < 0:
            raise ValueError("Initial balance must be non-negative")

        account_id = uuid4()
        new_account = Account(
            account_id=account_id, type=account_type, balance=initial_balance
        )

        self._accounts_db[account_id] = new_account
        return new_account

    def debit_account(self, account_id: UUID, amount: float) -> Account:
        """Debit (subtract) an amount from an account."""
        if amount <= 0:
            raise ValueError("Debit amount must be positive")

        account = self.get_account(account_id)
        if not account:
            raise KeyError(f"Account with ID {account_id} not found")

        if account.balance < amount:
            raise ValueError(
                f"Insufficient funds - balance is {account.balance}, attempted to debit {amount}"
            )

        account.balance -= amount
        self._accounts_db[account_id] = account
        return account

    def credit_account(self, account_id: UUID, amount: float) -> Account:
        """Credit (add) an amount to an account."""
        if amount <= 0:
            raise ValueError("Credit amount must be positive")

        account = self.get_account(account_id)
        if not account:
            raise KeyError(f"Account with ID {account_id} not found")

        account.balance += amount
        self._accounts_db[account_id] = account
        return account


# Create a singleton instance of the account service
account_service = AccountService()
