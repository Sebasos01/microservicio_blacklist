import pytest
from flask import Flask, request
from app.auth import require_jwt

@pytest.fixture
def test_app():
    app = Flask(__name__)
    app.config['JWT_STATIC_TOKEN'] = 'mi_token_jwt_estatico'
    return app

def test_require_jwt_valid_token(test_app):
    @test_app.route('/test')
    @require_jwt
    def test_route():
        return "Success"

    with test_app.test_client() as client:
        response = client.get(
            '/test',
            headers={'Authorization': 'Bearer mi_token_jwt_estatico'}
        )
        assert response.status_code == 200
        assert response.data == b'Success'

def test_require_jwt_missing_token(test_app):
    @test_app.route('/test')
    @require_jwt
    def test_route():
        return "Success"

    with test_app.test_client() as client:
        response = client.get('/test')
        assert response.status_code == 401

def test_require_jwt_invalid_token(test_app):
    @test_app.route('/test')
    @require_jwt
    def test_route():
        return "Success"

    with test_app.test_client() as client:
        response = client.get(
            '/test',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        assert response.status_code == 401

def test_require_jwt_malformed_header(test_app):
    @test_app.route('/test')
    @require_jwt
    def test_route():
        return "Success"

    with test_app.test_client() as client:
        response = client.get(
            '/test',
            headers={'Authorization': 'InvalidFormat'}
        )
        assert response.status_code == 401 