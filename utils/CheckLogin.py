
from app.db.database import get_db
from app.db.models import User
from utils.Hashes import verify_password

db = next(get_db())


# Created for adminV2

def login_util(username:str , password: str) -> bool:


    user = db.query(User).filter(User.email == username).first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False


    return True

def set_user_state(username):

    user = db.query(User).filter(User.email == username).first()

    #? Fix This later by adding default image in database so no need this after that
    if user.image_path is None:
        user.image_path = 'https://cdn.discordapp.com/attachments/921633563810627588/1175350979202400267/image.png?ex=656ae9e6&is=655874e6&hm=002a637e7bcbf71940f99b778a16e15f6d7487ddd05d11be3020bf04eebae2e0&'

    return {'username': user.email, 'avatar': user.image_path}