"""Basic tests — run with: pytest tests/ -v"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Patch DB before importing app
with patch("sqlalchemy.create_engine"), \
     patch("sqlalchemy.orm.sessionmaker"), \
     patch("sqlalchemy.ext.declarative.declarative_base") as mock_base:
    mock_base.return_value.metadata.create_all = MagicMock()
    # We import inside the patch context so engine creation doesn't fail
    import importlib, main as app_module
    client = TestClient(app_module.app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_root_message():
    response = client.get("/")
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_endpoint_exists():
    # Health may fail DB in CI, but the endpoint itself must respond
    response = client.get("/health")
    assert response.status_code in (200, 500)


def test_post_data_schema():
    """Schema validation: missing fields → 422"""
    response = client.post("/data", json={})
    assert response.status_code == 422
