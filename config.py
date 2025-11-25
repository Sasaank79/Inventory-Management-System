import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-prod'
    
    # Database
    # Default to SQLite for local dev if no URL provided
    # For Production (Render), DATABASE_URL will be set to MySQL/PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///inventory.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection Pool Settings (SQLAlchemy defaults are usually good, but making them explicit)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET') or 'jwt-secret-key-change-in-prod'
