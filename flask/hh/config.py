import pathlib
from datetime import timedelta
BASE_DIR = pathlib.Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR/"data"/"db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'aasdzs324234qfdddfe3434sr324erdfzxf'
    JWT_SECRET_KEY = '123213rfsdg345324eqasdfgw3q42'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=3)
