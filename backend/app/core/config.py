"""Shared database configuration.

The process environment takes precedence over a local backend/.env file. The
local file is intended for developer machines and is excluded from version
control.
"""

import os
from dataclasses import dataclass
from pathlib import Path


def _load_local_database_url() -> None:
    """Load DATABASE_URL from backend/.env when it is not already set."""
    if os.environ.get("DATABASE_URL"):
        return

    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")
        if key.strip() == "DATABASE_URL" and separator:
            os.environ["DATABASE_URL"] = value.strip().strip('"').strip("'")
            return


def _get_database_url() -> str:
    _load_local_database_url()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required. Set it in the environment or backend/.env."
        )
    return database_url


@dataclass(frozen=True)
class Settings:
    database_url: str


settings = Settings(database_url=_get_database_url())
