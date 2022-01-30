"""empty message

Revision ID: 92aa4bc407e8
Revises: 885892d38d1f
Create Date: 2021-12-05 20:31:26.751649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92aa4bc407e8'
down_revision = '885892d38d1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios_cursos',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('curso_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['curso_id'], ['cursos.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'curso_id')
    )
    op.create_table('usuarios_materias',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('materia_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['materia_id'], ['materias.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'materia_id')
    )
    op.create_table('usuarios_topicos',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('topico_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['topico_id'], ['topicos.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'topico_id')
    )
    op.create_table('licoes_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('licao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['licao_id'], ['licoes.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'licao_id')
    )
    op.create_table('questoes_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['questao_id'], ['questoes.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'questao_id')
    )
    op.create_table('usuarios_licoes',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('licao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['licao_id'], ['licoes.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'licao_id')
    )
    op.create_table('usuarios_questoes',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['questao_id'], ['questoes.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'questao_id')
    )
    op.drop_table('licoes_topicos')
    op.drop_table('questoes_topicos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questoes_topicos',
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('questao_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['questao_id'], ['questoes.id'], name='questoes_topicos_questao_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='questoes_topicos_tag_id_fkey'),
    sa.PrimaryKeyConstraint('tag_id', 'questao_id', name='questoes_topicos_pkey')
    )
    op.create_table('licoes_topicos',
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('licao_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['licao_id'], ['licoes.id'], name='licoes_topicos_licao_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='licoes_topicos_tag_id_fkey'),
    sa.PrimaryKeyConstraint('tag_id', 'licao_id', name='licoes_topicos_pkey')
    )
    op.drop_table('usuarios_questoes')
    op.drop_table('usuarios_licoes')
    op.drop_table('questoes_tags')
    op.drop_table('licoes_tags')
    op.drop_table('usuarios_topicos')
    op.drop_table('usuarios_materias')
    op.drop_table('usuarios_cursos')
    # ### end Alembic commands ###