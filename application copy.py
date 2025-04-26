# application.py
import os
from app import create_app

env_config = os.getenv("FLASK_CONFIG", "config.ProductionConfig")
application = create_app(config_class=env_config)

if __name__ == "__main__":
    # Only for local dev/testing
    application.debug = True
    application.run()
