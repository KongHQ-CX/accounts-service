## API Usage

See the `examples/example_usage.py` script for a complete demonstration of how to use the API.

### Creating an Account

```python
import requests

account_request = {
    "type": "checking",  # or "savings"
    "initial_balance": 1000.00
}

response = requests.post(
    "http://localhost:8081/accounts",
    json=account_request
)
account = response.json()
account_id = account["account_id"]
```

### Crediting an Account

```python
credit_request = {
    "amount": 500.00
}

response = requests.post(
    f"http://localhost:8081/accounts/{account_id}/credit",
    json=credit_request
)
updated_account = response.json()
```

### Debiting an Account

```python
debit_request = {
    "amount": 200.00
}

response = requests.post(
    f"http://localhost:8081/accounts/{account_id}/debit",
    json=debit_request
)
updated_account = response.json()
```

## Docker Hub Deployment

This repository is set up to build and publish Docker images to Docker Hub.

1. Set your Docker Hub username in the Makefile:

```makefile
IMAGE_NAME := your-dockerhub-username/accounts
```

2. Build and push the image:

```bash
make publish
```

## Using with Kong API Gateway

This service is designed to be used with Kong API Gateway for demonstrations. Once deployed, you can:

1. Register the service with Kong
2. Set up routes
3. Apply plugins like rate limiting, authentication, etc.
4. Monitor API traffic

## License

MIT# Accounts Service

A simple RESTful API service for managing bank accounts, designed as a demonstration for Kong API Gateway tooling.

## Features

- Create checking and savings accounts
- Retrieve account details
- List all accounts
- Credit (deposit) funds to accounts
- Debit (withdraw) funds from accounts
- Health check endpoints
- Proper error handling

## Project Structure

```
.
├── accounts/              # Main package
│   ├── __init__.py
│   ├── api/               # API modules
│   │   ├── __init__.py
│   │   ├── models.py      # Pydantic models
│   │   └── routes.py      # Route definitions
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   └── account.py     # Account operations
│   └── main.py            # App entry point
├── examples/              # Example scripts
│   └── example_usage.py   # Demo script
├── tests/                 # Test directory
│   ├── __init__.py
│   ├── conftest.py        # Test fixtures
│   └── test_api.py        # API tests
├── Dockerfile             # Docker configuration
├── docker-compose.yaml    # Docker Compose setup
├── Makefile               # Build automation
├── pyproject.toml         # Poetry config
└── README.md              # This file
```

## Development Setup

### Prerequisites

- Python 3.11+
- Poetry (Python package manager)
- Docker & Docker Compose (for containerization)

### Local Development

1. Install dependencies:

```bash
make setup
```

2. Run the service locally:

```bash
make run
```

3. Run tests:

```bash
make test
```

4. Lint code:

```bash
make lint
```

### Docker Development

1. Build the Docker image:

```bash
make docker-build
```

2. Run with Docker Compose:

```bash
make docker-compose-up
```

3. Stop Docker Compose services:

```bash
make docker-compose-down
```

## API Endpoints

- `GET /health` - Health check
- `GET /accounts` - List all accounts
- `POST /accounts` - Create a new account
- `GET /accounts/{account_id}` - Get account details
- `POST /accounts/{account_id}/debit` - Withdraw from account
- `POST /accounts/{account_id}/credit` - Deposit to account
