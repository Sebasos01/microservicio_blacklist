# application.py
import os
from app import create_app

env_config = os.getenv("FLASK_CONFIG", "config.ProductionConfig")
application = create_app(config_class=env_config)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
