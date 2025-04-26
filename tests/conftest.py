import pytest
from app import create_app
from app.extensions import db
from app.models import Blacklist

@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def valid_token():
    return "mi_token_jwt_estatico"

@pytest.fixture
def invalid_token():
    return "invalid_token"

@pytest.fixture
def sample_blacklist_entry():
    return {
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "reason": "Test reason"
    } 