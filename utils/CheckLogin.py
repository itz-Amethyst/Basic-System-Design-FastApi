
from app.db.database import get_db
from app.db.models import User
from utils.Hashes import verify_password


# Created for adminV2

def login_util(username:str , password: str) -> bool:

    db = next(get_db())

    user = db.query(User).filter(User.email == username).first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False


    return True
