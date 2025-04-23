.PHONY: setup install build test lint clean run docker-build docker-push docker-run docker-compose-up docker-compose-down

# Variables
IMAGE_NAME := kongcx/accounts-service
IMAGE_TAG := latest
PORT := 8081

# Setup development environment
setup:
	pip install poetry
	poetry install

# Install dependencies
install:
	poetry install

# Run tests
test:
	poetry run pytest tests/ --cov=accounts

# Lint the code
lint:
	poetry run isort accounts tests
	poetry run black accounts tests
	poetry run flake8 --ignore=E501 accounts tests

# Clean generated files
clean:
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +

# Run the application locally
run:
	poetry run uvicorn accounts.main:app --host 0.0.0.0 --port $(PORT) --reload

# Build Docker image
docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Push Docker image to registry
docker-push:
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

# Run Docker container
docker-run:
	docker run -p $(PORT):$(PORT) --name bank-account-service $(IMAGE_NAME):$(IMAGE_TAG)

# Start services using docker-compose
docker-compose-up:
	docker-compose up -d

# Stop services using docker-compose
docker-compose-down:
	docker-compose down

# Build and push the Docker image
publish: docker-build docker-push

# Full CI process
ci: lint test docker-build
