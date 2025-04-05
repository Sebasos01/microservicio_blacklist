# app/__init__.py
from flask import Flask
from .extensions import db  
from .routes import blacklist_bp  

def create_app(config_class="config.ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(blacklist_bp, url_prefix="/blacklists")

    with app.app_context():
        db.create_all()
    return app
