"""add users_confirmed

Revision ID: 293cc50c1b47
Revises: 6a7dcd1e227e
Create Date: 2023-05-22 10:57:45.663588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '293cc50c1b47'
down_revision = '6a7dcd1e227e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###