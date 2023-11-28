"""Added role options to user

Revision ID: 05e396b1a6dd
Revises: a5a521e8b41a
Create Date: 2023-11-28 17:08:38.159166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '05e396b1a6dd'
down_revision: Union[str, None] = 'a5a521e8b41a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    role_options = postgresql.ENUM('super_admin' , 'admin' , 'user' , name = 'role_options' ,
                                   create_type = False , )
    role_options.create(op.get_bind() , checkfirst = True , )
    op.add_column('Users' , sa.Column('role' , role_options , server_default = sa.text("'user'::role_options") , nullable = False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'role')
    role_options = postgresql.ENUM('super_admin' , 'admin' , 'user' , name = 'role_options' , create_type = False , )
    role_options.drop(op.get_bind() , checkfirst = True , )
    # ### end Alembic commands ###
