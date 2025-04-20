"""
Pydantic models for the Accounts API.
"""

from enum import Enum

from pydantic import UUID4, BaseModel, Field


class AccountType(str, Enum):
    """Type of bank account"""

    CHECKING = "checking"
    SAVINGS = "savings"


class ErrorCode(str, Enum):
    """Error codes for API responses"""

    INTERNAL_ERROR = "INTERNAL_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    INVALID_INPUT = "INVALID_INPUT"


class Account(BaseModel):
    """Account model representing a bank account"""

    account_id: UUID4
    type: AccountType
    balance: float


class CreateAccountRequest(BaseModel):
    """Request model for creating a new account"""

    type: AccountType
    initial_balance: float = Field(ge=0)


class UpdateBalanceRequest(BaseModel):
    """Request model for updating an account balance"""

    amount: float


class ErrorResponse(BaseModel):
    """Error response model"""

    error_code: ErrorCode
    message: str
