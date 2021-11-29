"""empty message

Revision ID: 7cb0d4b6d300
Revises: 0171b8cf9741
Create Date: 2021-07-12 04:22:24.060325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cb0d4b6d300'
down_revision = '0171b8cf9741'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('data_nascimento', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuarios', 'data_nascimento')
    # ### end Alembic commands ###