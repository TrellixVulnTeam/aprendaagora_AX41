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


# Página no Instagram
@bp.route('/')
def painel():
    return render_template('painel/index.html')
