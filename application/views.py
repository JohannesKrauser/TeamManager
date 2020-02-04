import csv
import tempfile
from os import environ
from os import path

from flask import Markup
from flask_admin import BaseView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from werkzeug import secure_filename


def gid_formatter(view, context, model, name):
    field = getattr(model, name)
    url = environ.get("SCD_URL")
    return Markup(f"<a href=\"#\" onClick=\"SCD=window.open('{url}{field}')\">{field}</a>")


class EmployeesView(ModelView):
    column_list = ("gid", "local_id", "name", "last_name")
    column_searchable_list = column_list
    column_formatters = {"gid": gid_formatter}
    form_create_rules = column_list
    form_edit_rules = column_list
    create_modal = True
    edit_modal = True


def accounts_formatter(view, context, model, name):
    field = getattr(model, name)
    display = ""

    if field:
        display += "<table class='table table-striped table-bordered table-hover model-list cf'>"
        for account in field:
            display += f"<tr><td>{account.name}</td></tr>"
        display += "</table>"

    return Markup(f"{display}")


class ProjectsView(ModelView):
    column_list = ("name", "accounts")
    column_searchable_list = ("name",)
    column_formatters = {"accounts": accounts_formatter}
    create_modal = True
    edit_modal = True


class AccountsView(ModelView):
    column_list = ("name", "start_date", "end_date", "order_amount", "project")
    column_searchable_list = ("name", "start_date", "end_date")
    form_create_rules = column_list
    form_edit_rules = column_list
    create_modal = True
    edit_modal = True


class TimeTracksView(ModelView):
    column_searchable_list = ("year", "month")
    create_modal = True
    edit_modal = True


class ImportFileForm(FlaskForm):
    file = FileField(validators=[FileRequired(), FileAllowed(["csv"])])


class ImportView(BaseView):
    @expose("/", methods=["GET", "POST"])
    def index(self):
        form = ImportFileForm()

        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            full_path = path.join(tempfile.gettempdir(), filename)
            form.file.data.save(full_path)

            parse_csv(full_path)

            return self.render("import.html", form=form)

        return self.render("import.html", form=form)


def parse_csv(file):
    output = {}

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")

        counter = -1
        for row in csv_reader:
            counter += 1

            if counter == 0:
                continue

            employee_local_id = int(row[3])
            account_name = row[7]
            hours = float(row[13])

            if account_name == "SUM":
                # Sick leave
                hours = float(row[14])
                if hours > 0:
                    account_name = "SICK LEAVE"
                    create_time_track(account_name, employee_local_id, hours)

                # Education leave
                hours = float(row[15])
                if hours > 0:
                    account_name = "EDUCATION LEAVE"
                    create_time_track(account_name, employee_local_id, hours)

                # Holiday abroad
                hours = float(row[16])
                if hours > 0:
                    account_name = "HOLIDAY ABROAD"
                    create_time_track(account_name, employee_local_id, hours)

                # Parental leave
                hours = float(row[17])
                if hours > 0:
                    account_name = "PARENTAL LEAVE"
                    create_time_track(account_name, employee_local_id, hours)

                # Vacation leave
                hours = float(row[18])
                if hours > 0:
                    account_name = "VACATION LEAVE"
                    create_time_track(account_name, employee_local_id, hours)
            else:
                create_time_track(account_name, employee_local_id, hours)

    return output


def create_time_track(account_name, employee_local_id, hours):
    from .database import db
    from sqlalchemy.orm.exc import NoResultFound
    from .models import Employee
    from .models import Account
    from .models import TimeTrack

    try:
        employee = db.session.query(Employee).filter_by(local_id=employee_local_id).one()
        account = db.session.query(Account).filter_by(name=account_name).one()
    except NoResultFound:
        return

    time_track = TimeTrack()
    time_track.account_id = account.id
    time_track.employee_id = employee.id
    time_track.hours = hours
