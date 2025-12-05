import pytest
from app import create_app

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        # here is where you would connect a staging (test) DB if you wanted to
        "SQLALCHEMY_DATABASE_URI": "postgresql://user:pass@localhost/db_name"
    })
    yield app

@pytest.fixture
def client(app):
    """Test client for making requests"""
    return app.test_client()
