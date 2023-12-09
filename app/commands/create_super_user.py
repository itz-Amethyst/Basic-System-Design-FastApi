import asyncclick as click
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import RoleOptions , User
from email_validator import validate_email

from utils.Hashes import hash_password

db: Session = next(get_db())


#! Need to work on it
@click.command()
@click.option("-e", "--email", type=str, required = True)
@click.option("-p", "--password", type=str, required = True)
@click.option("-r", "--role", type=str, required = False)
def create_user(email: str, password: str, role: str):

    if role is None:
        role = "super_admin"

    if validate_email(email) is False:
        raise RuntimeError("email is not valid")

    print(role)
    if role.lower() not in RoleOptions.__members__:
        raise RuntimeError("Role Not Valid please select between : user, super_admin, admin")

    check_user = db.query(User).filter(User.email == email).first()

    if check_user:
        raise RuntimeError(f"User with this email {email} already exists")

    password = hash_password(password)

    new_user: User = User(email = email , password = password , image_path = 'G:/Fast Api/Basic System/Uploads/d4c92f13ff1627393532043.jpg' ,
                          size = 0 , ext = "unknown" , mime = "unknown", role = role)
    db.add(new_user)
    db.commit()
    click.echo("User Successfully created!")


if __name__ == "__main__":
    create_user(_anyio_backend = "asyncio")