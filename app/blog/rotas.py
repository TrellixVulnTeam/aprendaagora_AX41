# Blueprint BLOG

from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from . import blog as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Role, Permissao, Publicacao, Tag, Comentario, PublicacaoAmei
from ..email import enviar_email
from ..formularios import formularioPublicacaoBlog

#from ..formularios import formularioPublicacaoBlog

from ..funcoes_auxiliares import criar_artigo, registrar_comentario, truncar_texto


# Página inicial do BLOG
@bp.route('/')
def inicio():

    #artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.id >= 5))
    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.id >= 5)).order_by(desc(Publicacao.data)).all()
    
    return render_template('blog/index.html', artigos=artigos)



# Rota para um Professor escrever no Blog
@bp.route('/escrever', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def escrever_publicacao():

    formulario = formularioPublicacaoBlog()


    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit():

        try:

            artigo = criar_artigo(formulario)

            db.session.add(artigo)

            db.session.commit()

            flash("Artigo criado com sucesso", 'alert-success')

        except:
            flash("Um erro ocorreu durante a criação do artigo", 'alert-danger')

        return redirect(url_for('blog.inicio'))
        

    return render_template('blog/escrever.html', formulario=formulario)




@bp.route('/artigo/<int:id_artigo>', methods=['GET'])
def artigo(id_artigo):

    artigo = Publicacao.query.filter_by(id=id_artigo).first_or_404()

    return render_template('blog/artigo.html', artigo=artigo)




# Página de SÉRIES
@bp.route('/series')
def series():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'series')).all()

    return render_template('blog/index.html', artigos=artigos)


# Página de VIAGEM
@bp.route('/viagem')
def viagem():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'viagem')).all()

    return render_template('blog/index.html', artigos=artigos)


# Página de BRASIL
@bp.route('/brasil')
def brasil():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'brasil')).all()

    return render_template('blog/index.html', artigos=artigos)


# Página de ESTUDO
@bp.route('/estudo')
def estudo():
    
    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'estudo')).all()

    return render_template('blog/index.html', artigos=artigos)



# Página de ENTREVISTAS
@bp.route('/entrevistas')
def entrevistas():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'entrevistas')).all()

    return render_template('blog/index.html', artigos=artigos)

