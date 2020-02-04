import warnings

from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate

from .database import db
from .views import AccountsView
from .views import EmployeesView
from .views import ProjectsView
from .views import TimeTracksView
from .views import ImportView


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
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Fields missing from ruleset", UserWarning)
            admin.add_view(EmployeesView(models.Employee, db.session, name="Employees", url="/employees"))
            admin.add_view(
                ProjectsView(models.Project, db.session, name="Projects", url="/projects", category="Projects"))
            admin.add_view(
                AccountsView(models.Account, db.session, name="Accounts", url="/accounts", category="Projects"))
            admin.add_view(ImportView(name="Import", url="/import", category="Time Tracks"))
            admin.add_view(
                TimeTracksView(models.TimeTrack, db.session, name="List", url="/time_tracks", category="Time Tracks"))

        return app
