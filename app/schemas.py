# app/schemas.py
from .extensions import ma
from marshmallow import fields, validate

class BlacklistSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    app_uuid = fields.Str(required=True)
    reason = fields.Str(validate=validate.Length(max=255), allow_none=True)
    ip_address = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
