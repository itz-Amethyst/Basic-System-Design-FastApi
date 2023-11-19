from sqladmin import Admin, ModelView
from app.main import app
from app.db.database import engine
from app.db.models import User



admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = "__all__"


admin.add_view(UserAdmin)