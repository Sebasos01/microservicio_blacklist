# application.py
import os
from app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

env_config = os.getenv("FLASK_CONFIG", "config.ProductionConfig")
application = create_app(config_class=env_config)

application.wsgi_app = ProxyFix(application.wsgi_app, x_for=1, x_proto=1)

if __name__ == "__main__":
    # Only for local dev/testing
    application.run(host="0.0.0.0", port=8000)
