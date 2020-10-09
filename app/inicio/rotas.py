# Blueprint Início

from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required
from datetime import datetime
from . import inicio as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Permissao
from ..email import enviar_email


""" ROTAS """

# Página de Login
@bp.route('/', methods=['GET', 'POST'])
def inicio():
    # Se o método for GET
    return render_template('inicio.html', current_time=datetime.utcnow())











# Rota do painel do Administrador

# De forma prática, o decorador 'route' deve ser declarado primeiro quando se está usando vários decoradores em uma função view. Os decoradores restantes devem ser declarados na orde que eles precisam ser avaliado quando a função view for chamada. Neste caso, o usuário deve estar conectado primeiro, considerando que o usuário deve ser redirecionado para a página de login caso ele não esteja conectado.
@bp.route('/admin')
@login_required
@admin_necessario
def apenas_admins():
    return "Apenas Administradores!"


# Rota para escrever no Blog
@bp.route('/escrever')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def apenas_professores():
    return "Apenas Professores!"


