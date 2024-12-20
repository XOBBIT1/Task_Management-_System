"""User password, email

Revision ID: 758aef918409
Revises: 98af6aa205a4
Create Date: 2024-11-12 14:00:41.891831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '758aef918409'
down_revision: Union[str, None] = '98af6aa205a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('password', sa.String(), nullable=True))
    op.add_column('Users', sa.Column('email', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'email')
    op.drop_column('Users', 'password')
    # ### end Alembic commands ###
