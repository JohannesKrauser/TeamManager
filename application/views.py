from flask import Markup
from flask_admin.contrib.sqla import ModelView
from os import environ

def gid_formatter(view, context, model, name):
    field = getattr(model, name)
    url = environ.get("SCD_URL")
    return Markup(f"<a href=\"#\" onClick=\"SCD=window.open('{url}{field}')\">{field}</a>")


class EmployeeAdminView(ModelView):
    column_list = ("gid", "local_id", "name", "last_name")
    column_searchable_list = ("gid", "local_id", "name", "last_name")
    column_sortable_list = ("gid", "local_id", "name", "last_name")
    column_formatters = {"gid": gid_formatter}
    create_modal = True
    edit_modal = True
