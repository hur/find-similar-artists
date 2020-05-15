import os
import uuid

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SHOW_DIALOG = False
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URL = os.environ.get('SPOTIFY_CALLBACK_URL') or "http://127.0.0.1:5000/callback"


class TestConfig(Config):
    # Override certain variables for tests
    SECRET_KEY = str(uuid.uuid4().hex)
    SHOW_DIALOG = True
