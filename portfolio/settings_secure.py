import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Securely load configuration
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')

# ... rest of your settings ...
