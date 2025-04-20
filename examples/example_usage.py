"""
Example usage of the Accounts API.
This script demonstrates how to interact with the API using the requests library.
"""

import json
import uuid
import requests

BASE_URL = "http://localhost:8081"


def pretty_print_json(data):
    """Utility function to pretty print JSON responses"""
    print(json.dumps(data, indent=2))


def main():
    """Main function demonstrating API usage"""
    print("1. CHECKING API HEALTH")
    print("-" * 50)
    health_response = requests.get(f"{BASE_URL}/health")
    print(f"Health check status: {health_response.status_code}")
    print(f"Response: {health_response.text}")
    print()

    print("2. CREATING A CHECKING ACCOUNT")
    print("-" * 50)
    checking_account_request = {"type": "checking", "initial_balance": 1000.00}

    create_checking_response = requests.post(
        f"{BASE_URL}/accounts", json=checking_account_request
    )
    checking_account = create_checking_response.json()
    checking_account_id = checking_account["account_id"]

    print(f"Created checking account, status: {create_checking_response.status_code}")
    print("Checking account details:")
    pretty_print_json(checking_account)
    print()

    print("3. CREATING A SAVINGS ACCOUNT")
    print("-" * 50)
    savings_account_request = {"type": "savings", "initial_balance": 5000.00}

    create_savings_response = requests.post(
        f"{BASE_URL}/accounts", json=savings_account_request
    )
    savings_account = create_savings_response.json()
    savings_account_id = savings_account["account_id"]

    print(f"Created savings account, status: {create_savings_response.status_code}")
    print("Savings account details:")
    pretty_print_json(savings_account)
    print()

    print("4. LISTING ALL ACCOUNTS")
    print("-" * 50)
    list_accounts_response = requests.get(f"{BASE_URL}/accounts")
    accounts = list_accounts_response.json()

    print(f"List accounts, status: {list_accounts_response.status_code}")
    print("All accounts:")
    pretty_print_json(accounts)
    print()

    print("5. GETTING CHECKING ACCOUNT DETAILS")
    print("-" * 50)
    get_checking_response = requests.get(f"{BASE_URL}/accounts/{checking_account_id}")
    checking_details = get_checking_response.json()

    print(f"Get checking account details, status: {get_checking_response.status_code}")
    print("Checking account details:")
    pretty_print_json(checking_details)
    print()

    print("6. DEBITING THE CHECKING ACCOUNT")
    print("-" * 50)
    debit_request = {"amount": 200.00}

    debit_response = requests.post(
        f"{BASE_URL}/accounts/{checking_account_id}/debit", json=debit_request
    )
    updated_checking = debit_response.json()

    print(f"Debit checking account, status: {debit_response.status_code}")
    print("Updated checking account after debit:")
    pretty_print_json(updated_checking)
    print()

    print("7. CREDITING THE SAVINGS ACCOUNT")
    print("-" * 50)
    credit_request = {"amount": 500.00}

    credit_response = requests.post(
        f"{BASE_URL}/accounts/{savings_account_id}/credit", json=credit_request
    )
    updated_savings = credit_response.json()

    print(f"Credit savings account, status: {credit_response.status_code}")
    print("Updated savings account after credit:")
    pretty_print_json(updated_savings)
    print()

    print("8. ATTEMPTING TO DEBIT MORE THAN AVAILABLE BALANCE (ERROR CASE)")
    print("-" * 50)
    excessive_debit_request = {"amount": 10000.00}

    excessive_debit_response = requests.post(
        f"{BASE_URL}/accounts/{checking_account_id}/debit", json=excessive_debit_request
    )

    print(f"Excessive debit attempt, status: {excessive_debit_response.status_code}")
    print("Error response:")
    pretty_print_json(excessive_debit_response.json())
    print()

    print("9. ATTEMPTING TO ACCESS NON-EXISTENT ACCOUNT (ERROR CASE)")
    print("-" * 50)
    nonexistent_id = str(uuid.uuid4())
    nonexistent_response = requests.get(f"{BASE_URL}/accounts/{nonexistent_id}")

    print(f"Non-existent account access, status: {nonexistent_response.status_code}")
    print("Error response:")
    pretty_print_json(nonexistent_response.json())
    print()


if __name__ == "__main__":
    main()
