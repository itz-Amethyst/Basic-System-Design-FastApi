from dataclasses import dataclass

from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from starlette.middleware import Middleware
from starlette.responses import RedirectResponse
from starlette_admin.exceptions import FormValidationError, LoginFailed

from utils.CheckLogin import login_util

@dataclass
class AdminConfig:
    is_authenticated: bool = False

class AdminAuth(AuthenticationBackend):



    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form['username'], form['password']

        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if login_util(username , password) is not False:
            """Save `username` in session"""
            # request.session.update(set_user_state(username))
            # request.state.user = set_user_state(username)
            AdminConfig.is_authenticated = True
            request.session.update({'token': "test"})
            return True

        return False

    async def authenticate( self , request ) -> bool:
        # if request.session.get("username" , None):
        if AdminConfig.is_authenticated is True:

            # request.state.user = request.session["username"]
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        AdminConfig.is_authenticated = False
        return True


