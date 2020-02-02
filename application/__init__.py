from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate

from .database import db


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

        Migrate(app, db)
        # Terminal
        # flask db init
        # flask db migrate
        # flask db upgrade

        admin = Admin(app, url="/")

        return app
