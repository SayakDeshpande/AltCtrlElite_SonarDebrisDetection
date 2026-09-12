"""Minimal FastAPI application for the SIH26057 backend."""

from fastapi import FastAPI

# Importing the engine reads the shared database configuration but does not
# open a PostgreSQL connection. Connections are opened only when the engine is
# used by a future request handler.
from app.db.session import engine as _engine  # noqa: F401
from app.api.router import api_router


app = FastAPI(title="SIH26057 Backend")
app.include_router(api_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Return a process-health response without querying PostgreSQL."""
    return {"status": "ok"}
