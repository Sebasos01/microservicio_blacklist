# app/models.py
from datetime import datetime
from .extensions import db
from sqlalchemy.sql import func

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    app_uuid = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())