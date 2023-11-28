import enum
from datetime import datetime

from sqlalchemy import Column , String , TIMESTAMP , Integer , Enum
from sqlalchemy.sql.expression import text
from app.db.database import Base
from utils.CustomMethods import generate_generic_id

class RoleOptions(enum.Enum):
    super_admin = "super admin"
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = 'Users'

    #! Imp Note: It's not set on server default in db so whenever you create a custom data in db  dont except to auto generate id ( without parentheses will run in every request )
    id = Column(String, primary_key = True, nullable = False, unique = True, default = generate_generic_id)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'), default = datetime.now())
    size = Column(Integer, nullable = False, server_default = text('0'))
    mime = Column(String, nullable = False, server_default = 'Unknown')
    ext = Column(String, nullable = False, server_default = 'Unknown')
    image_path = Column(String, nullable = True)

    role = Column(Enum(RoleOptions), nullable = False, server_default = RoleOptions.user.value)

