from starlette.requests import Request
from app.db.models.user import RoleOptions
from app.shared.errors import permission_excepted

def is_admin(request: Request):
    user = request.state.user

    if not user or user.role not in (RoleOptions.admin.value, RoleOptions.super_admin.value):
        raise permission_excepted