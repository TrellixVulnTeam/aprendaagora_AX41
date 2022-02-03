from flask import (
    jsonify,
    request,
    g,
    url_for,
    current_app,
)

from . import api
from ..modelos import Usuario, Permissao
from .decoradores import permissao_necessaria
from .. import db
from .erros import proibido


@api.route('/usuarios/')
def selecionar_usuarios():
    
    usuarios = Usuario.query.all()

    return jsonify({ 'usuarios': [usuario.to_json() for usuario in usuarios]})

@api.route('/usuarios/paginado')
def selecionar_usuarios_paginado():

    pagina = request.args.get('pagina', 1, type=int)

    paginacao = Usuario.query.paginate(
        pagina,
        per_page=current_app.config['MURAL_PUBLICACOES_POR_PAGINA'],
        error_out=False
    )

    usuarios = paginacao.items()

    anterior = None

    if paginacao.has_prev:
        anterior = url_for('api.selecionar_usuarios_paginado', pagina=pagina-1)
    
    proximo = None

    if paginacao.has_next:
        proximo = url_for('api.selecionar_usuarios_paginado', pagina=pagina+1)

    return jsonify({
        'usuarios': [usuario.to_json() for usuario in usuarios],
        'url_anterior': anterior,
        'url_proximo': proximo,
        'contador': paginacao.total
    })


@api.route('/usuarios/<int:id>')
def selecionar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    return jsonify(usuario.to_json())

