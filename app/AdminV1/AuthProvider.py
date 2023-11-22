from dataclasses import dataclass
from typing import Optional

from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from utils.CheckLogin import login_util, set_user_state


@dataclass
class AdminConfig:
    logo_url: Optional[str] = None
    app_title: Optional[str] = None
    is_authenticated: bool = False


#! -----------------------> Very very bullshit login system BUT IT"S OK : ) <-------------------------

class Auth_Admin_Provider(AuthProvider):
    """
        This is for demo purpose, it's not a better
        way to save and validate user credentials
        """

    async def login(
            self ,
            username: str ,
            password: str ,
            remember_me: bool ,
            request: Request ,
            response: Response ,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )


        if login_util(username, password) is not False:
            """Save `username` in session"""
            request.session.update(set_user_state(username))
            request.state.user = set_user_state(username)
            AdminConfig.is_authenticated = True
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated( self , request ) -> bool:
        # if request.session.get("username" , None):
        if AdminConfig.is_authenticated is True:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            # request.state.user = request.session["username"]
            return True

        return False

    def get_admin_config( self , request: Request ) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        custom_app_title = "Hello, " + user["name"] + "!"
        # Update logo url according to current_user
        custom_logo_url = None
        if user.get("company_logo_url" , None):
            custom_logo_url = request.url_for("static" , path = user["company_logo_url"])
        return AdminConfig(
            app_title = custom_app_title ,
            logo_url = custom_logo_url ,
        )

    def get_admin_user( self , request: Request ) -> AdminUser:
        # user = request.state.user  # Retrieve current user
        user = request.session.items().mapping
        # photo_url = None
        # if user["avatar"] is None:
            # photo_url = request.url_for("static" , path = user["avatar"])

        return AdminUser(username = user["username"] , photo_url = user['avatar'])

    async def logout( self , request: Request , response: Response ) -> Response:
        request.session.clear()
        AdminConfig.is_authenticated = False
        return response