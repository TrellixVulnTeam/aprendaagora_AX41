from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..modelos import Publicacao, Permissao, Comentario
from . import api
from .decoradores import permissao_necessaria


@api.route('/comentarios/')
def selecionar_comentarios():

    page = request.args.get('page', 1, type=int)

    pagination = Comentario.query.order_by(Comentario.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comentarios = pagination.items

    anterior = None

    if pagination.has_prev:
        anterior = url_for('api.selecionar_comentarios', page=page-1)

    proximo = None

    if pagination.has_next:
        proximo = url_for('api.selecionar_comentarios', page=page+1)

    return jsonify({
        'comentarios': [comentario.to_json() for comentario in comentarios],
        'anterior': anterior,
        'proximo': proximo,
        'count': pagination.total
    })


@api.route('/comentarios/<int:id>')
def selecionar_comentario(id):
    comentario = Comentario.query.selecionar_or_404(id)
    return jsonify(comentario.to_json())


@api.route('/publicacoes/<int:id>/comentarios/')
def selecionar_publicacao_comentarios(id):

    publicacao = Publicacao.query.selecionar_or_404(id)

    page = request.args.get('page', 1, type=int)
    
    pagination = publicacao.comentarios.order_by(Comentario.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    
    comentarios = pagination.items
    
    anterior = None
    
    if pagination.has_prev:
        anterior = url_for('api.selecionar_publicacao_comentarios', id=id, page=page-1)
    
    proximo = None
    
    if pagination.has_next:
        proximo = url_for('api.selecionar_publicacao_comentarios', id=id, page=page+1)
    
    return jsonify({
        'comentarios': [comentario.to_json() for comentario in comentarios],
        'anterior': anterior,
        'proximo': proximo,
        'count': pagination.total
    })


@api.route('/publicacoes/<int:id>/comentarios/', methods=['POST'])
@permissao_necessaria(Permissao.COMENTAR)
def novo_publicacao_comentario(id):

    publicacao = Publicacao.query.selecionar_or_404(id)
    
    comentario = Comentario.from_json(request.json)
    
    comentario.autor = g.current_user
    
    comentario.publicacao = publicacao
    
    db.session.add(comentario)
    
    db.session.commit()
    
    return jsonify(comentario.to_json()), 201, \
        {'Location': url_for('api.selecionar_comentario', id=comentario.id)}