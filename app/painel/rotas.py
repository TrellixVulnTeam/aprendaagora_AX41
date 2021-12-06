# Blueprint PAINEL

from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import painel as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import InscricaoFeuRosa, Usuario, Role, Permissao, Publicacao, Tag, UsuarioAnonimo
from ..email import enviar_email



#from .formularios import

###########################################################################################


# PAINEL
@bp.route('/')
def painel():
    return render_template('painel/index.html')

# PAINEL
@bp.route('/criar_artigo')
def criar_artigo():
    return render_template('painel/criar_artigo.html')


    # PAINEL
@bp.route('/listar_artigos')
def listar_artigos():
    return render_template('painel/criar_artigo.html')


# PAINEL
@bp.route('/criar_licao')
def criar_licao():
    return render_template('painel/criar_licao.html')

# PAINEL
@bp.route('/listar_licoes')
def listar_licoes():
    return render_template('painel/criar_licao.html')


# PAINEL
@bp.route('/criar_questao')
def criar_questao():
    return render_template('painel/criar_questao.html')

# PAINEL
@bp.route('/listar_questoes')
def listar_questoes():
    return render_template('painel/criar_questao.html')




# PAINEL
@bp.route('/criar_topico')
def criar_topico():
    return render_template('painel/criar_topico.html')

# PAINEL
@bp.route('/listar_topicos')
def listar_topicos():
    return render_template('painel/criar_topico.html')


# PAINEL
@bp.route('/criar_curso')
def criar_curso():
    return render_template('painel/criar_topico.html')



# PAINEL
@bp.route('/listar_cursos')
def listar_cursos():
    return render_template('painel/criar_topico.html')
