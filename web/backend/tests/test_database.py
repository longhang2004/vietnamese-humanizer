import runpy
from pathlib import Path

import pytest

from app.config import settings


@pytest.mark.parametrize(
    ("scheme", "expected_drivers"),
    [
        ("postgresql+psycopg", ("psycopg",)),
        ("postgresql+psycopg2", ("psycopg2",)),
        ("postgresql", ("psycopg", "psycopg2")),
        ("postgres", ("psycopg", "psycopg2")),
    ],
)
def test_database_module_loads_postgresql_driver_without_connecting(
    monkeypatch, scheme, expected_drivers
):
    monkeypatch.setattr(settings, "DATABASE_URL", f"{scheme}://test:test@localhost/test")

    # Load the real startup code independently of the SQLite engine used by other tests.
    namespace = runpy.run_path(str(Path(__file__).parents[1] / "app/db/database.py"))
    engine = namespace["engine"]
    try:
        assert engine.dialect.name == "postgresql"
        assert engine.dialect.driver in expected_drivers
    finally:
        engine.dispose()
