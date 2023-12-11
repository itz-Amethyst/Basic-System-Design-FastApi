from fastapi import Depends

from app.managers.auth import oauth2_password , AuthManager
from app.shared import errors


# Check if user is logged in
def user_required( token: str = Depends(oauth2_password) ):
    return AuthManager.verify_access_token(token , errors.credentials_exception)
