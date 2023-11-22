from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.views import Link , DropDown

from app.db.models import User , Parent
from app.db.database import engine
from starlette_admin._types import RowActionsDisplayType
from app.AdminV1.AuthProvider import Auth_Admin_Provider

# https://jowilf.github.io/starlette-admin/


class CustomModelView(ModelView):
    # page_size = 5

    page_size_options = [2 , 4 , 6 , 8 , -1]

    row_actions_display_type = RowActionsDisplayType.DROPDOWN


    # exclude_fields_from_list: List of fields to exclude from the List page.
    # exclude_fields_from_detail: List of fields to exclude from the Detail page.
    # exclude_fields_from_create: List of fields to exclude from the creation page.
    # exclude_fields_from_edit: List of fields to exclude from the editing page.\

    #> No Use
    # sortable_fields = [User.id]
    searchable_fields = [User.email]


# You can apply customs here
admin = Admin(engine,
              title = "Dr_Stop",
              base_url = "/admin2",
              logo_url = "`https`://preview.tabler.io/static/logo-white.svg" ,
              login_logo_url = "`https`://preview.tabler.io/static/logo.svg" ,
              auth_provider = Auth_Admin_Provider(),
              middlewares = [Middleware(SessionMiddleware, secret_key = '1234')]
              )


# admin.add_view(ModelView(User, icon = 'fa fa-lock'))
admin.add_view(CustomModelView(User, icon = 'fa fa-lock'))

# Add to menu => show in admin or not
admin.add_view(CustomView(label="Home", icon="fa fa-home", path="/home", template_path="home.html" , add_to_menu = True))

# Custom Link to exit admin or whatever
admin.add_view(Link(label="Home Page", icon="fa fa-link", url="/"))
#
admin.add_view(
    DropDown(
        "Resources",
        icon="fa fa-car",
        views=[
            # Note: Icon cant change here
            ModelView(Parent , icon='fa fa-lock'),
            Link(label="Home Page", url="/"),
            CustomView(label="Dashboard", path="/dashboard", template_path="dashboard.html"),
        ],
    )
)


# No Need
# admin.mount_to(app)