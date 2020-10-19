# Blueprint INGLÊS

from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify
from flask_login import login_required, current_user

from . import ingles as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Role, Permissao, Publicacao, Tag
from ..email import enviar_email
from ..formularios import formularioPublicacaoMural
from ..funcoes_auxiliares import criar_publicacao


# Página inicial de INGLÊS
@bp.route('/', methods=['GET', 'POST'])
def inicio():
    
    # Seleciona o formulário
    formulario = formularioPublicacaoMural(idioma="ingles")

    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit() and current_user.pode(Permissao.ESCREVER_MURAL):

        # Cria a publicação
        publicacao = criar_publicacao(formulario)

        # Adiciona a publicação è sessão do banco de dados
        db.session.add(publicacao)

        # Salva as alterações no banco de dados
        db.session.commit()

        # Redireciona para a página do idioma INGLÊS
        return redirect(url_for('ingles.inicio'))


    pagina = request.args.get('pagina', 1, type=int)

    paginacao = db.session.query(Publicacao, Usuario).join(Usuario).order_by(Publicacao.data.desc()).paginate(
        pagina, per_page=current_app.config['MURAL_PUBLICACOES_POR_PAGINA'],
        error_out=False)
    
    

    publicacoes = paginacao.items


    def truncarTexto(texto):

        if len(texto) > 200:
            texto = texto[0:200] + '...'

        return texto



    for publicacao in publicacoes:

        texto = publicacao[0].conteudo

        publicacao[0].conteudo = truncarTexto(texto)

        print(publicacao[0].conteudo)


    # Seleciona todas as publicações (ao mesmo tempo vinculando o autor de cada publicação)
    # A consulta ao banco de dados retorna uma lista de elementos do tipo 'sqlalchemy.util._collections.result' (?). Cada um destes, por sua vez, possuem duas instâncias, uma do modelo Publicacao e outra do modelo Usuario 
    
    
    #publicacoes = db.session.query(Publicacao, Usuario).join(Usuario).order_by(Publicacao.data.desc()).all()

    # Exibe a página do idioma INGLÊS, enviando o formulário do mural e a lista de publicações
    return render_template('ingles.html', formulario=formulario, publicacoes=publicacoes, paginacao=paginacao)


@bp.route('/publicacao/json', methods=['GET', 'POST'])
def modal_publicacao():

    try:
        # Seleciona o JSON enviado através do pedido do cliente
        json_enviado = request.get_json()

        # Converte e armazena a propriedade 'publicacao_id' para um int
        publicacao_id = int(json_enviado['publicacao_id'])

        # Consulta o banco de dados e seleciona a publicação cujo id foi enviado pelo pedido
        publicacao = Publicacao.query.filter_by(id=publicacao_id).first()

        # Seleciona o representação da publicação em formato JSON
        publicacao_json = publicacao.json()

        # Responde o cliente, enviando a publicação em formato JSON
        return jsonify(publicacao_json)

    except Exception as e:

        print("AJAX exceção " + str(e))
        return(str(e))
