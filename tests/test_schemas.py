import datetime
import pytest
from app.schemas import BlacklistSchema

def test_blacklist_schema_validation():
    schema = BlacklistSchema()
    
    # Test valid data
    valid_data = {
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "reason": "Test reason"
    }
    result = schema.load(valid_data)
    assert result["email"] == valid_data["email"]
    assert result["app_uuid"] == valid_data["app_uuid"]
    assert result["reason"] == valid_data["reason"]

def test_blacklist_schema_invalid_email():
    schema = BlacklistSchema()
    
    invalid_data = {
        "email": "invalid-email",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000"
    }
    
    with pytest.raises(Exception):
        schema.load(invalid_data)

def test_blacklist_schema_missing_required_fields():
    schema = BlacklistSchema()
    
    invalid_data = {
        "email": "test@example.com"
    }
    
    with pytest.raises(Exception):
        schema.load(invalid_data)

def test_blacklist_schema_reason_length():
    schema = BlacklistSchema()
    
    # Test reason that's too long
    invalid_data = {
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "reason": "a" * 256  # Exceeds 255 character limit
    }
    
    with pytest.raises(Exception):
        schema.load(invalid_data)

def test_blacklist_schema_dump():
    schema = BlacklistSchema()
    
    data = {
        "id": 1,
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "reason": "Test reason",
        "ip_address": "127.0.0.1",
        "created_at": datetime.datetime(2024, 1, 1),
    }
    
    result = schema.dump(data)
    assert "id" in result
    assert "email" in result
    assert "app_uuid" in result
    assert "reason" in result
    assert "ip_address" in result
    assert "created_at" in result 