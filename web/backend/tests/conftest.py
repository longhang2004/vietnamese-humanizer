from collections.abc import Generator
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import models  # noqa: F401 - registers models on Base.metadata
from app.db.database import Base, get_db
from app.limiter import limiter
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def disable_limiter():
    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest.fixture(scope="function")
def db_session() -> Generator:
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Generator) -> Generator:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_gemini():
    with patch("app.services.rewriter.genai.Client") as mock_client_cls:
        mock_client_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Bản dịch/viết lại đã được gọt giũa tự nhiên hơn."
        mock_client_instance.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client_instance
        yield mock_client_instance
