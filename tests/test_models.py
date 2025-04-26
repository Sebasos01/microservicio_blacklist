import pytest
from datetime import datetime
from app.models import Blacklist
from app.extensions import db

def test_blacklist_model_creation(app, sample_blacklist_entry):
    with app.app_context():
        entry = Blacklist(
            email=sample_blacklist_entry["email"],
            app_uuid=sample_blacklist_entry["app_uuid"],
            reason=sample_blacklist_entry["reason"],
            ip_address="127.0.0.1"
        )
        db.session.add(entry)
        db.session.commit()
        
        assert entry.email == sample_blacklist_entry["email"]
        assert entry.app_uuid == sample_blacklist_entry["app_uuid"]
        assert entry.reason == sample_blacklist_entry["reason"]
        assert entry.ip_address == "127.0.0.1"
        
        assert isinstance(entry.created_at, datetime)

def test_blacklist_model_required_fields(app):
    with app.app_context():
        with pytest.raises(Exception):
            # Create a Blacklist instance without required fields
            entry = Blacklist()
            db.session.add(entry)
            db.session.commit()

def test_blacklist_model_save(app, sample_blacklist_entry):
    with app.app_context():
        entry = Blacklist(
            email=sample_blacklist_entry["email"],
            app_uuid=sample_blacklist_entry["app_uuid"],
            reason=sample_blacklist_entry["reason"],
            ip_address="127.0.0.1"
        )
       
        db.session.add(entry)
        db.session.commit()
        
        saved_entry = Blacklist.query.filter_by(email=sample_blacklist_entry["email"]).first()
        assert saved_entry is not None
        assert saved_entry.email == sample_blacklist_entry["email"]
        assert saved_entry.app_uuid == sample_blacklist_entry["app_uuid"]
        assert saved_entry.reason == sample_blacklist_entry["reason"] 