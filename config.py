# config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_STATIC_TOKEN = os.getenv("JWT_STATIC_TOKEN", "token_estatico")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")

class ProductionConfig(Config):
    db_host = os.getenv('RDS_HOSTNAME')
    db_user = os.getenv('RDS_USERNAME')
    db_pass = os.getenv('RDS_PASSWORD')
    db_name = os.getenv('RDS_DB_NAME')
    db_port = os.getenv('RDS_PORT', '5432')

    if db_host and db_user and db_pass and db_name:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///prod.db")
