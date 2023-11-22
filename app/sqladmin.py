from typing import Any
from fastapi import Request
import wtforms
from sqladmin import Admin, ModelView
from app.main import app
from app.db.database import engine
from app.db.models import User , Parent

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    page_size = 2
    page_size_options = [2 , 4 , 6 , 8 , 10]

    column_list = "__all__"
    #! Note: First need to be just exclude one and you can define 1 row to be excluded and it will show rest
    # column_exclude_list = [User.id]
    column_details_exclude_list = [User.id]

    icon = 'fa fa-wifi'
    category = 'Accounts'

    column_sortable_list = [User.email, User.id, User.created_at, User.created_at]
    column_searchable_list = [User.email, User.id]

    #! can use to short description in blog part like to show only first 10 letter or whatever
    # column_formatters = {User.email: lambda m , a: m.email[:10]}


    column_labels = {User.password: "Hashed Password", User.created_at: "Register Date"}


    # Columns inside edit/create form
    # form_columns = []

    # To Change label inside edit/create form -> replace email with name of column
    form_args = dict(email=dict(label = 'Full Email'))

    # Can make it readonly
    form_widget_args = dict(password=dict(readonly=True))

    # Validation field for email
    form_overrides = dict(email=wtforms.EmailField)

    # form_include_pk = True

    #! Note: the create/edit forms are customizable you can delete save and create new button in here venv/Lib/site-packages/sqladmin/templates/create.html

    # can_export = bool
    # can_create = bool
    # can_edit = bool
    # can_delete = bool
    # can_view_details = bool

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:

        # print(request.base_url)
        print(request.url)

class ParentAdmin(ModelView, model = Parent):
    icon = 'fa fa-list'

    # Can be both in same category!
    category = 'Accounts'


admin.add_view(UserAdmin)
admin.add_view(ParentAdmin)