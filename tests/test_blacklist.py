import json
import pytest
from app.models import Blacklist

def test_health_check(client):
    response = client.get("/blacklists/health")
    assert response.status_code == 200
    assert response.json == {"status": "OK"}

def test_add_to_blacklist_missing_token(client, sample_blacklist_entry):
    response = client.post(
        "/blacklists/",
        json=sample_blacklist_entry
    )
    assert response.status_code == 401

def test_add_to_blacklist_invalid_token(client, invalid_token, sample_blacklist_entry):
    response = client.post(
        "/blacklists/",
        json=sample_blacklist_entry,
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
    assert response.status_code == 401

def test_add_to_blacklist_valid(client, valid_token, sample_blacklist_entry):
    response = client.post(
        "/blacklists/",
        json=sample_blacklist_entry,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 201
    data = response.json
    assert "message" in data
    assert "data" in data
    assert data["data"]["email"] == sample_blacklist_entry["email"]
    assert data["data"]["app_uuid"] == sample_blacklist_entry["app_uuid"]
    assert data["data"]["reason"] == sample_blacklist_entry["reason"]

def test_add_to_blacklist_invalid_email(client, valid_token):
    response = client.post(
        "/blacklists/",
        json={
            "email": "invalid-email",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000"
        },
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 400

def test_add_to_blacklist_missing_required_fields(client, valid_token):
    response = client.post(
        "/blacklists/",
        json={"email": "test@example.com"},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 400

def test_check_blacklist_missing_token(client):
    response = client.get("/blacklists/test@example.com")
    assert response.status_code == 401

def test_check_blacklist_invalid_token(client, invalid_token):
    response = client.get(
        "/blacklists/test@example.com",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
    assert response.status_code == 401

def test_check_blacklist_not_found(client, valid_token):
    response = client.get(
        "/blacklists/nonexistent@example.com",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert response.json == {
        "blacklisted": False,
        "email": "nonexistent@example.com"
    }

def test_check_blacklist_found(client, valid_token, sample_blacklist_entry):
    # First add an entry
    client.post(
        "/blacklists/",
        json=sample_blacklist_entry,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Then check it
    response = client.get(
        f"/blacklists/{sample_blacklist_entry['email']}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    data = response.json
    assert data["blacklisted"] == True
    assert data["email"] == sample_blacklist_entry["email"]
    assert data["reason"] == sample_blacklist_entry["reason"]
    assert data["app_uuid"] == sample_blacklist_entry["app_uuid"]
    assert "created_at" in data 