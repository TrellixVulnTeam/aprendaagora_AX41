"""empty message

Revision ID: 458d35aca468
Revises: cfb9eb6a86da
Create Date: 2021-12-05 21:18:32.248067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '458d35aca468'
down_revision = 'cfb9eb6a86da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comentarios', sa.Column('questao_id', sa.Integer(), nullable=True))
    op.drop_constraint('comentarios_publicacao_id_fkey', 'comentarios', type_='foreignkey')
    op.create_foreign_key(None, 'comentarios', 'questoes', ['questao_id'], ['id'])
    op.create_foreign_key(None, 'comentarios', 'topicos', ['publicacao_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comentarios', type_='foreignkey')
    op.drop_constraint(None, 'comentarios', type_='foreignkey')
    op.create_foreign_key('comentarios_publicacao_id_fkey', 'comentarios', 'publicacoes', ['publicacao_id'], ['id'])
    op.drop_column('comentarios', 'questao_id')
    # ### end Alembic commands ###
