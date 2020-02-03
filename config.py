from os import environ
from os import path
from dotenv import load_dotenv

load_dotenv()


class Config:
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    uri_base = environ.get("SQLALCHEMY_DATABASE_URI_BASE")
    database_name = environ.get("SQLALCHEMY_DATABASE_NAME")
    root_directory = path.dirname(path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = f"{uri_base}{path.join(root_directory, database_name)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
