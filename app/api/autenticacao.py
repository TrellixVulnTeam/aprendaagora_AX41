from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..modelos import Usuario
from . import api
from .erros import nao_autorizado, proibido


autorizacao = HTTPBasicAuth()


@autorizacao.verify_password
def verificar_senha(email_ou_token, senha):
    if email_ou_token == '':
        return False
    if senha == '':
        g.current_user = Usuario.verificar_token_autorizacao(email_ou_token)
        g.token_usado = True
        return g.current_user is not None

    usuario = Usuario.query.filter_by(email=email_ou_token).first()

    if not usuario:
        return False

    g.current_user = usuario
    g.token_usado = False

    return usuario.verificar_senha(senha)



@autorizacao.error_handler
def erro_autorizacao():
    return nao_autorizado('Credenciais inválidas.')


# Decorador aplicado a todas as rotas do api antes de executar o pedido para autenticar usuários anônimos e 
@api.before_request
@autorizacao.login_required
def antes_do_pedido():
    if not g.current_user.is_anonymous and \
        not g.current_user.confirmado:
        return proibido('Conta não confirmada.')


@api.route('/tokens/', methods=['POST'])
def get_tokens():
    if g.current_user.is_anonymous or g.token_usado:
        return nao_autorizado('Credenciais inválidas.')

    return jsonify({'token': g.current_user.gerar_token_autorizacao(expiracao=3600), 'expiracao': 3600})