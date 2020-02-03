from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate

from .database import db
from .views import EmployeeAdminView


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

        from . import models
        Migrate(app, db)
        # Terminal
        # flask db init
        # flask db migrate
        # flask db upgrade

        admin = Admin(app, url="/")
        admin.add_view(EmployeeAdminView(models.Employee, db.session, name="Employees", url="/employees"))

        return app
