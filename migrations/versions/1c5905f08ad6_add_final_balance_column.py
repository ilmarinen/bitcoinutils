"""Add final balance column.

Revision ID: 1c5905f08ad6
Revises: 04ca42deac5c
Create Date: 2020-07-19 01:13:39.286283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c5905f08ad6'
down_revision = '04ca42deac5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('final_balance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('addresses', 'final_balance')
    # ### end Alembic commands ###