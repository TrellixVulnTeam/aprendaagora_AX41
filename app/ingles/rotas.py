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


    # Seleciona o número da página a partir do pedido
    pagina = request.args.get('pagina', 1, type=int)

    # Seleciona as publicações do mural (ao mesmo tempo vinculando o autor de cada publicação) e pagina elas (divide em porções)
    # A consulta ao banco de dados retorna uma lista de elementos do tipo 'sqlalchemy.util._collections.result' (?). Cada um destes, por sua vez, possuem duas instâncias, uma do modelo Publicacao e outra do modelo Usuario 
    paginacao = db.session.query(Publicacao, Usuario).join(Usuario).order_by(Publicacao.data.desc()).paginate(
        pagina, per_page=current_app.config['MURAL_PUBLICACOES_POR_PAGINA'],
        error_out=False)
    

    # Seleciona as publicações da página selecionada
    # paginacao.items representa os itens da página atual na paginação
    # Os itens da paginação são do tipo 'sqlalchemy.util._collections.result' (?). Cada um destes, por sua vez, possuem duas instâncias, uma do modelo Publicacao e outra do modelo Usuario 
    publicacoes = paginacao.items

    # Limita a quantidade de caracteres de uma string em 200 caracteres
    def truncar_texto(texto):
        # Se a string possuir mais de 200 caracteres
        if len(texto) > 200:
            # Fatie os primeiros 200 caracteres da string e adicione "..." no final
            texto = texto[0:200] + '...'
        

        # Retorne a string truncado
        return texto

    # Para cada publicação na lista de publicações, trunque o texto
    for publicacao in publicacoes:

        if publicacao[0].conteudo_html:
            texto = publicacao[0].conteudo_html
            publicacao[0].conteudo_html = truncar_texto(texto)
        else:
            texto = publicacao[0].conteudo
            publicacao[0].conteudo = truncar_texto(texto)

    # Exibe a página do idioma INGLÊS, enviando o formulário do mural e a lista de publicações
    return render_template('ingles.html', formulario=formulario, publicacoes=publicacoes, paginacao=paginacao)


# Página de uma publicação
@bp.route('/publicacao/<int:id>')
def publicacao(id):

    # Seleciona uma publicação com o id informado
    publicacao = Publicacao.query.get_or_404(id)

    # Exibe a página da publicação
    return render_template('publicacao.html', publicacao=publicacao)


@bp.route('/publicacao/editar', methods=['POST'])
def editar_publicacao():

    try:
            # Seleciona o JSON enviado através do pedido do cliente
            json_enviado = request.get_json()

            """
            # Converte e armazena a propriedade 'publicacao_id' para um int
            publicacao_id = int(json_enviado['publicacao_id'])
            """

            
            publicacao_id = json_enviado["publicacao_id"]
            publicacao_titulo = json_enviado["publicacao_titulo"]
            publicacao_conteudo = json_enviado["publicacao_conteudo"]

            print(publicacao_id)
            print(publicacao_titulo)
            print(publicacao_conteudo)


            publicacao = Publicacao.query.get_or_404(publicacao_id)

            if current_user != publicacao.autor:
                abort(404)

            publicacao.titulo = publicacao_titulo

            publicacao.conteudo = publicacao_conteudo

            db.session.add(publicacao)

            db.session.commit()


            confirmar_comunicacao = {"confirmado": True}
            return  jsonify(confirmar_comunicacao)

    except Exception as e:

        print("AJAX exceção " + str(e))
        return(str(e))


    #Publicacao.query.get_or_404(id).


# Rota que retorna um objeto JSON representando as informações (que o usuário não consegue acessar localmente) da publicação
# Esta rota é usada pela funcionalidade de modal
@bp.route('/publicacao/json', methods=['GET', 'POST'])
def json_publicacao():

    try:
        # Seleciona o JSON enviado através do pedido do cliente
        json_enviado = request.get_json()

        # Converte e armazena a propriedade 'publicacao_id' para um int
        publicacao_id = int(json_enviado['publicacao_id'])

        # Consulta o banco de dados e seleciona a publicação cujo id foi enviado pelo pedido
        publicacao = Publicacao.query.filter_by(id=publicacao_id).first()

        # Seleciona o representação da publicação em formato JSON
        publicacao_json = publicacao.json()

        print(current_user.id)
        publicacao_json['autor_cliente'] = (current_user.id == publicacao_json['id_autor'])
        print(publicacao_json)

        # Responde o cliente, enviando a publicação em formato JSON
        return jsonify(publicacao_json)

    except Exception as e:

        print("AJAX exceção " + str(e))
        return(str(e))
