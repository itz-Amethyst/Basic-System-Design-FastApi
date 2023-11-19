from starlette_admin.contrib.sqla import Admin, ModelView
from app.db.models import User
from app.db.database import engine

# https://jowilf.github.io/starlette-admin/

admin = Admin(engine , title = 'Test Admin')
admin.add_view(ModelView(User))

# No Need
# admin.mount_to(app)