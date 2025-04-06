# app/routes.py
from flask import Blueprint, request, jsonify
from .models import Blacklist
from .extensions import db  
from .schemas import BlacklistSchema
from .auth import require_jwt
from datetime import datetime

blacklist_bp = Blueprint("blacklists", __name__)
blacklist_schema = BlacklistSchema()
blacklist_list_schema = BlacklistSchema(many=True)

@blacklist_bp.route("/", methods=["POST"])
@require_jwt
def add_to_blacklist():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        data = blacklist_schema.load(json_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    entry = Blacklist(
        email=data["email"],
        app_uuid=data["app_uuid"],
        reason=data.get("reason"),
        ip_address=request.remote_addr
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify({
        "message": "Email agregado a la lista negra", 
        "data": blacklist_schema.dump(entry)
    }), 201

@blacklist_bp.route("/<string:email>", methods=["GET"])
@require_jwt
def check_blacklist(email):
    entry = Blacklist.query.filter_by(email=email).first()
    if not entry:
        return jsonify({"blacklisted": False, "email": email}), 200

    return jsonify({
        "blacklisted": True,
        "email": entry.email,
        "reason": entry.reason,
        "app_uuid": entry.app_uuid,
        "created_at": entry.created_at.isoformat()
    }), 200

# Nuevo endpoint para health check
@blacklist_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200
