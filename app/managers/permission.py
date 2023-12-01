from fastapi.requests import Request

from app import schemas
from app.db.models.user import RoleOptions
from app.shared.errors import permission_excepted

class PermissionManager:

    @staticmethod
    def set_session_user( request: Request , data: schemas.TokenData ):
        result = request.session['user'] = data

        return result

    def is_admin( self: Request ):
        user = self.session.get('user')

        if not user or user['role'] not in (RoleOptions.admin.value , RoleOptions.super_admin.value):
            raise permission_excepted