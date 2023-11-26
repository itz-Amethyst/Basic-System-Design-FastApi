import enum
from datetime import datetime

from sqlalchemy import Column , Integer , String , TIMESTAMP , ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.db.database import Base
from app.db.models.user import User


#! Note! whenever you had enum option system use this example code inside alembic migration to fix error

#  status = postgresql.ENUM('type1', 'type2', name='status', create_type=False)
#  status.create(op.get_bind(), checkfirst=True)
#  op.add_column('company', sa.Column('type', status, nullable=True))

#* be careful to start with lowercase always !
class StatusOptions(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Parent(Base):
    __tablename__ = 'Parents'

    id = Column(Integer , primary_key = True , nullable = False)
    title = Column(String , nullable = False)
    status = Column(Enum(StatusOptions), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True) , nullable = False , server_default = text('now()') ,
                        default = datetime.now())
    owner_id = Column(String , ForeignKey(User.id , ondelete = "CASCADE") , nullable = False)

    owner = relationship(User)

