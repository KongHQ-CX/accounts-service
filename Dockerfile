# Use Python 3.11 slim as base image
FROM python:3.11-slim AS builder

# Install Poetry with the same version as your local environment
RUN pip install --no-cache-dir poetry==2.1.2

# Set working directory
WORKDIR /app

# Copy project files needed for installation
COPY pyproject.toml ./
COPY poetry.lock ./
COPY README.md ./

# Use Poetry to install dependencies without installing the project itself
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-root

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create accounts directory - this must happen before copying files
RUN mkdir -p /app/accounts

# Copy application code
COPY accounts/ ./accounts/
COPY README.md ./

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose API port
EXPOSE 8081

# Run the application
CMD ["uvicorn", "accounts.main:app", "--host", "0.0.0.0", "--port", "8081"]
