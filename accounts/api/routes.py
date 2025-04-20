"""
API routes for the Accounts Service.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, status

from accounts.api.models import (
    Account,
    CreateAccountRequest,
    ErrorCode,
    ErrorResponse,
    UpdateBalanceRequest,
)
from accounts.services.account import account_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get(
    "",
    operation_id="listAccounts",
    summary="List all accounts",
    response_model=List[Account],
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Failed to retrieve accounts due to internal \
            server error",
        }
    },
)
def list_accounts():
    """Returns a list of all accounts with basic details."""
    try:
        return account_service.list_accounts()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": ErrorCode.INTERNAL_ERROR,
                "message": (
                    "Lock error: failed to acquire lock while listing accounts"
                ),
            },
        )


@router.post(
    "",
    operation_id="createAccount",
    summary="Create a new account",
    response_model=Account,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Failed to create account due to invalid input",
        },
        500: {
            "model": ErrorResponse,
            "description": ("Failed to create account due to internal" "server error"),
        },
    },
)
def create_account(account_request: CreateAccountRequest):
    """Creates a new account with an initial balance. The account ID is automatically generated."""
    try:
        return account_service.create_account(
            account_type=account_request.type,
            initial_balance=account_request.initial_balance,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": ErrorCode.INVALID_INPUT,
                "message": f"Failed to create account: {str(e)}",
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": ErrorCode.INTERNAL_ERROR,
                "message": "Failed to create account: Internal server error occurred",
            },
        )


@router.get(
    "/{account_id}",
    operation_id="getAccountById",
    summary="Retrieve a single account",
    response_model=Account,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Account lookup failed - specified account ID does not exist",
        },
        500: {
            "model": ErrorResponse,
            "description": "Failed to retrieve account details due to internal server error",
        },
    },
)
def get_account_by_id(
    account_id: UUID = Path(..., description="The UUID of the account to retrieve")
):
    """Returns details for the specified account including current balance."""
    try:
        account = account_service.get_account(account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error_code": ErrorCode.NOT_FOUND,
                    "message": f"Failed to retrieve account: ID {account_id} not found",
                },
            )
        return account
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": ErrorCode.INTERNAL_ERROR,
                "message": "Failed to retrieve account: Internal server error occurred",
            },
        )


@router.post(
    "/{account_id}/debit",
    operation_id="debitAccount",
    summary="Debit an account",
    response_model=Account,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Debit operation failed due to insufficient funds or invalid amount",
        },
        404: {
            "model": ErrorResponse,
            "description": "Debit operation failed - account not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Failed to process debit operation due to internal server error",
        },
    },
)
def debit_account(
    update_request: UpdateBalanceRequest,
    account_id: UUID = Path(..., description="The UUID of the account to debit"),
):
    """Decreases the account's balance by the specified amount."""
    try:
        return account_service.debit_account(account_id, update_request.amount)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": ErrorCode.NOT_FOUND,
                "message": "Failed to debit account: Account does not exist",
            },
        )
    except ValueError as e:
        if "Insufficient funds" in str(e):
            error_code = ErrorCode.INSUFFICIENT_FUNDS
        else:
            error_code = ErrorCode.INVALID_INPUT

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": error_code,
                "message": f"Failed to debit account: {str(e)}",
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": ErrorCode.INTERNAL_ERROR,
                "message": "Failed to debit account: Internal server error occurred",
            },
        )


@router.post(
    "/{account_id}/credit",
    operation_id="creditAccount",
    summary="Credit an account",
    response_model=Account,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Credit operation failed due to invalid amount",
        },
        404: {
            "model": ErrorResponse,
            "description": "Credit operation failed - account not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Failed to process credit operation due to internal server error",
        },
    },
)
def credit_account(
    update_request: UpdateBalanceRequest,
    account_id: UUID = Path(..., description="The UUID of the account to credit"),
):
    """Increases the account's balance by the specified amount."""
    try:
        return account_service.credit_account(account_id, update_request.amount)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": ErrorCode.NOT_FOUND,
                "message": "Failed to credit account: Account does not exist",
            },
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": ErrorCode.INVALID_INPUT,
                "message": f"Failed to credit account: {str(e)}",
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": ErrorCode.INTERNAL_ERROR,
                "message": "Failed to credit account: Internal server error occurred",
            },
        )
