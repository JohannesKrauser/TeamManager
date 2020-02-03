from flask import Markup
from flask_admin.contrib.sqla import ModelView
from os import environ


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


class ProjectsView(ModelView):
    column_list = ("name", "accounts")
    column_searchable_list = ("name",)
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
