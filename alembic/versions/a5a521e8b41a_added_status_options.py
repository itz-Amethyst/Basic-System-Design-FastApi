"""Added status options

Revision ID: a5a521e8b41a
Revises: 27be978c986b
Create Date: 2023-11-26 19:20:55.277895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a5a521e8b41a'
down_revision: Union[str, None] = '27be978c986b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    parent_statuses = postgresql.ENUM('accepted' , 'pending' , 'rejected' , name = 'parent_statuses' ,
                                      create_type = False , )
    parent_statuses.create(op.get_bind() , checkfirst = True , )
    op.add_column('Parents' , sa.Column('status' , parent_statuses , nullable = True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Parents', 'status')
    # ### end Alembic commands ###
