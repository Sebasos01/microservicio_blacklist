# app/auth.py
import os
from functools import wraps
from flask import request, abort

JWT_STATIC_TOKEN = os.getenv("JWT_STATIC_TOKEN", "mi_token_jwt_estatico")

def require_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if token != JWT_STATIC_TOKEN:
            abort(401, description="Unauthorized - Invalid Token")

        return f(*args, **kwargs)
    return wrapper
