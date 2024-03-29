"""hash_password

Revision ID: d82d4134f9df
Revises: 9b53699ee7e2
Create Date: 2024-02-18 18:09:33.099261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd82d4134f9df'
down_revision: Union[str, None] = '9b53699ee7e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hashed_password', postgresql.BYTEA(), nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.drop_column('users', 'hashed_password')
    # ### end Alembic commands ###
