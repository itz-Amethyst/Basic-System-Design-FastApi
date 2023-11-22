from typing import Any
from fastapi import Request
import wtforms
from sqladmin import Admin, ModelView
from app.main import app
from app.db.database import engine
from app.db.models import User , Parent
from app.Admin_SQLAlchemy.AdminAuth import AdminAuth

logo_url = "https://cdn.discordapp.com/attachments/921633563810627588/1175350979202400267/image.png?ex=656ae9e6&is=655874e6&hm=002a637e7bcbf71940f99b778a16e15f6d7487ddd05d11be3020bf04eebae2e0&"



admin = Admin(app , engine , title = 'SQLADMIN BASHE ?!' , logo_url = logo_url , authentication_backend = AdminAuth(secret_key = 'Test'))


class UserAdmin(ModelView, model=User):
    page_size = 5
    page_size_options = [3 , 5 , 7 , 9 , 11]

    column_list = "__all__"
    #! Note: First need to be just exclude one and you can define 1 row to be excluded and it will show rest
    # column_exclude_list = [User.id]
    column_details_exclude_list = [User.id]

    icon = 'fa fa-wifi'
    category = 'Accounts'

    column_sortable_list = [User.email, User.id, User.created_at, User.created_at]
    column_searchable_list = [User.email, User.id]

    # Default sorting
    column_default_sort = ("created_at", True)

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