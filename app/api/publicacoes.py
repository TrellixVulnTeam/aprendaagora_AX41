from flask import (
    jsonify,
    request,
    g,
    url_for,
    current_app,
)

from . import api
from ..modelos import Publicacao, Permissao, Usuario
from .decoradores import permissao_necessaria
from .. import db
from .erros import proibido


@api.route('/publicacoes/')
def selecionar_publicacoes():
    
    publicacoes = Publicacao.query.all()

    return jsonify({ 'publicacoes': [publicacao.to_json() for publicacao in publicacoes]})

@api.route('/publicacoes/paginado')
def selecionar_publicacoes_paginado():

    pagina = request.args.get('pagina', 1, type=int)

    paginacao = Publicacao.query.paginate(
        pagina,
        per_page=current_app.config['MURAL_PUBLICACOES_POR_PAGINA'],
        error_out=False
    )

    publicacoes = paginacao.items()

    anterior = None

    if paginacao.has_prev:
        anterior = url_for('api.selecionar_publicacoes_paginado', pagina=pagina-1)
    
    proximo = None

    if paginacao.has_next:
        proximo = url_for('api.selecionar_publicacoes_paginado', pagina=pagina+1)

    return jsonify({
        'publicacoes': [publicacao.to_json() for publicacao in publicacoes],
        'url_anterior': anterior,
        'url_proximo': proximo,
        'contador': paginacao.total
    })


@api.route('/publicacoes/<int:id>')
def selecionar_publicacao(id):

    publicacao = Publicacao.query.get_or_404(id)

    return jsonify(publicacao.to_json())


@api.route('/publicacoes/', methods=['POST'])
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def nova_publicacao():

    publicacao = Publicacao.from_json(request.json)

    publicacao.autor = g.current_user

    db.session.add(publicacao)

    db.session.commit()

    return jsonify(publicacao.to_json()), 201, {'Location': url_for('api.selecionar_publicacao', id=publicacao.id)}



@api.route('/publicacoes/', methods=['PUT'])
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def editar_publicacao(id):

    publicacao = Publicacao.query.get_or_404(id)

    if g.current_user != publicacao.autor and \
        not g.current_user.pode(Permissao.ADMIN):
        
        return proibido('O usuário não possui permissão para essa ação.')
    
    publicacao.conteudo = request.json.get('conteudo', publicacao.conteudo)

    db.session.add(publicacao)

    db.session.commit()

    return jsonify(publicacao.to_json())


@api.route('/publicacoes/<int:id>', methods=['DELETE'])
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def apagar_publicacao(id):

    Publicacao.query.filter_by(id=id).delete()

    db.session.commit()

    return jsonify({'sucesso': True})



@api.route('/usuarios/<int:id>/publicacoes', methods=['POST'])
def selecionar_usuario_publicacoes(id):

    usuario = Usuario.query.selecionar_or_404(id)

    page = request.args.get('page', 1, type=int)
    
    pagination = usuario.publicacoes.order_by(Publicacao.data_criacao.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    
    publicacoes = pagination.items
    
    anterior = None
    
    if pagination.has_prev:
        anterior = url_for('api.selecionar_usuario_publicacoes', id=id, page=page-1)
    
    proximo = None
    
    if pagination.has_next:
        proximo = url_for('api.selecionar_usuario_publicacoes', id=id, page=page+1)
    
    return jsonify({
        'publicacoes': [publicacao.to_json() for publicacao in publicacoes],
        'anterior': anterior,
        'proximo': proximo,
        'count': pagination.total
    })