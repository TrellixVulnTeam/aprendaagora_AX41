# Blueprint BLOG

from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from . import blog as bp
from .formularios import formularioArtigoBlog, formularioComentarioArtigo

from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Role, Permissao, Publicacao, Tag, Comentario, PublicacaoAmei
from ..email import enviar_email
from ..funcoes_auxiliares import criar_artigo, registrar_comentario, truncar_texto

from flask_uploads import UploadSet, IMAGES

fotos = UploadSet('photos', IMAGES)

"""
    ROTAS


    inicio()

    escrever_artigo()

    editar_artigo(id_artigo)

    artigo(id_artigo)

    series()

    viagem()

    brasil()

    estudo()

    entrevistas()
"""




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
def escrever_artigo():

    formulario = formularioArtigoBlog()

    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit():

        try:
            # Seleciona a foto
            foto = request.files['foto']

            # Formata o nome do arquivo
            nome_arquivo = foto.filename
            nome_arquivo2 = nome_arquivo.replace("'", "")
            nome_arquivo3 = nome_arquivo2.replace(" ", "_")
            
            # Se a extensão do arquivo for permitida
            if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                # Tenta salvar a foto em app/static/image/produto
                salvar_foto = fotos.save(foto, folder="cabecalho")
                
                # Se a foto tiver sido salva corretamente
                if salvar_foto:

                    artigo = criar_artigo(formulario, nome_arquivo3)

                    db.session.add(artigo)

                    db.session.commit()

            flash("Artigo criado com sucesso", 'alert-success')

        except:
            flash("Um erro ocorreu durante a criação do artigo", 'alert-danger')

        return redirect(url_for('blog.inicio'))
        

    return render_template('blog/escrever.html', formulario=formulario)





"""
!!! NÃO FOI IMPLEMENTADA
"""
# Página que edita um artigo
@bp.route('/editar/<int:id_artigo>', methods=['GET'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def editar_artigo(id_artigo):

    artigo = Publicacao.query.filter_by(id=id_artigo).first_or_404()

    return render_template('blog/artigo.html', artigo=artigo)



# Página que exibe um artigo
@bp.route('/artigo/<int:artigo_id>', methods=['GET', 'POST'])
def artigo(artigo_id):

    artigo = Publicacao.query.filter_by(id=artigo_id).first_or_404()

    formulario = formularioComentarioArtigo()

    if formulario.validate_on_submit():

        try:

            # Registra o comentário no banco de dados
            registrar_comentario(
                artigo_id,
                current_user.id,
                formulario.conteudo.data
            )

            flash("Seu comentário foi publicado")
            return redirect(url_for('.artigo', artigo_id=artigo.id, pagina=-1))
        except (erro):
            flash("Um erro ocorreu durante a criação do comentário")
            return redirect(url_for('.artigo', artigo_id=artigo.id, pagina=-1))

    pagina = request.args.get('pagina', 1, type=int)

    if pagina == -1:

        pagina = (artigo.comentarios.count() - 1) // current_app.config['ARTIGO_COMENTARIOS_POR_PAGINA'] + 1

    paginacao = artigo.comentarios.order_by(Comentario.data.asc()).paginate(
            pagina, per_page=current_app.config['ARTIGO_COMENTARIOS_POR_PAGINA'],
            error_out=False
        )

    comentarios = paginacao.items

    return render_template(
        'blog/artigo.html',
        artigo=artigo,
        formulario=formulario,
        comentarios=comentarios,
        paginacao=paginacao
    )




##################
# SEÇÕES DO BLOG #
##################

# Página de SÉRIES
@bp.route('/series')
def series():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'series')).all()

    return render_template('blog/index.html', artigos=artigos, assunto='Séries')


# Página de VIAGEM
@bp.route('/viagem')
def viagem():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'viagem')).all()

    return render_template('blog/index.html', artigos=artigos, assunto='Viagem')


# Página de BRASIL
@bp.route('/brasil')
def brasil():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'brasil')).all()

    return render_template('blog/index.html', artigos=artigos, assunto='Brasil')


# Página de ESTUDO
@bp.route('/estudo')
def estudo():
    
    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'estudo')).all()

    return render_template('blog/index.html', artigos=artigos, assunto='Estudo')


# Página de ENTREVISTAS
@bp.route('/entrevistas')
def entrevistas():

    artigos = Publicacao.query.filter(Publicacao.tags.any(Tag.nome == 'entrevistas')).all()

    return render_template('blog/index.html', artigos=artigos, assunto='Entrevistas')

