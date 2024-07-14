import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ALLOWED_EXTENSIONS = {'pdf'}