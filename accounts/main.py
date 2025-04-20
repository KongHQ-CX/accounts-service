"""
Entry point for the Accounts API.
A demonstration microservice for Kong API Gateway tooling.
"""

import uvicorn
from fastapi import FastAPI

from accounts.api.routes import router

app = FastAPI(
    title="Accounts API",
    description="This API manages Kong Bank account information and balances. Used for Kong tooling demonstrations.",
    version="1.0.0",
)

app.include_router(router)


@app.get(
    "/health",
    tags=["health"],
    operation_id="healthCheck",
    summary="Health check endpoint",
)
def health_check():
    """Returns the API's health status"""
    return "Accounts API is running"


@app.head(
    "/health",
    tags=["health"],
    operation_id="healthCheckHead",
    summary="Health check endpoint (HEAD)",
)
def health_check_head():
    """Returns the API's health status without body"""
    return None


def main():
    """Run the application with uvicorn"""
    uvicorn.run(app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    main()
