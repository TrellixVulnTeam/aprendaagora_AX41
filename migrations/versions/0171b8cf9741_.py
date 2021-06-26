"""empty message

Revision ID: 0171b8cf9741
Revises: 5db635889b59
Create Date: 2021-06-20 19:56:33.332925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0171b8cf9741'
down_revision = '5db635889b59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publicacoes_amei',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('publicacao_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['publicacao_id'], ['publicacoes.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publicacoes_amei')
    # ### end Alembic commands ###