from starlette.requests import Request
from app.db.models.user import RoleOptions
from app.shared.errors import permission_excepted

class PermissionManager:
    def is_admin( self: Request ):
        user = self.state.user

        if not user or user.role not in (RoleOptions.admin.value , RoleOptions.super_admin.value):
            raise permission_excepted