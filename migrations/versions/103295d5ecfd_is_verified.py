"""IS verified

Revision ID: 103295d5ecfd
Revises: f6059148a27f
Create Date: 2024-11-15 13:54:42.246985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '103295d5ecfd'
down_revision: Union[str, None] = 'f6059148a27f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('is_verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'is_verified')
    # ### end Alembic commands ###
