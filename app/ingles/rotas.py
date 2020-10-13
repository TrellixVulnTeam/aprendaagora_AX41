# Blueprint INGLÊS

from flask import render_template, session, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import ingles as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Role, Permissao, Publicacao
from ..email import enviar_email
from ..formularios import formularioPublicacaoMural



@bp.route('/', methods=['GET', 'POST'])
def inicio():
    
    formulario = formularioPublicacaoMural(idioma="ingles")

    if current_user.pode(Permissao.ESCREVER_MURAL) and formulario.validate_on_submit():

        # TRANSFORMAR A CRIAÇÃO DE UMA PUBLICAÇÃO EM UMA FUNÇÃO QUANDO FOR CRIAR OS BLUEPRINTS DOS OUTROS IDIOMAS POR QUE ESTE TRECHO SERÁ IGUAL
        publicacao = Publicacao(
            titulo=formulario.titulo.data,
            conteudo=formulario.conteudo.data,
            idioma=formulario.idioma,
            autor=current_user._get_current_object()
            )

        # Imprime as tags selecionadas
        print(formulario.tags.data)

        # PSEUDOCÓDIGO DA INSERÇÃO DE REGISTROS NA TABELA publicacao_tag
        """
        Para cada tag selecionada no formulário
            
            # Inserir um registro na tabela 'publicacoes_tags' com o id da tag e o id do post
            
            # Seleciona a tag no banco de dados de acordo com o que foi selecionado
            t = Tag.query.filter_by(id=tag.id)

            # Adiciona a tag selecionada à lista de tags da publicação
            publicacao.tags.append(t)
        """

        db.session.add(publicacao)
        db.session.commit()
        return redirect(url_for('ingles.inicio'))
    
    publicacoes = db.session.query(Publicacao, Usuario).join(Usuario).order_by(Publicacao.data.desc()).all()

    return render_template('ingles.html', formulario=formulario, publicacoes=publicacoes)
