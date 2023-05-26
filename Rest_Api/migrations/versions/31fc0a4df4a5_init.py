"""Init

Revision ID: 31fc0a4df4a5
Revises: 7a3807ec4bcb
Create Date: 2023-05-08 13:46:47.051952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31fc0a4df4a5'
down_revision = '7a3807ec4bcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column(
        'created_at', sa.DateTime(), nullable=True))
    op.add_column('contacts', sa.Column(
        'updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'updated_at')
    op.drop_column('contacts', 'created_at')
    # ### end Alembic commands ###
