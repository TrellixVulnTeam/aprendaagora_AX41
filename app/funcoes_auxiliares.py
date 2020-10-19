from flask_login import current_user
from .modelos import Publicacao, Tag

# Esta função cria uma publicação após receber um pedido POST, de um cliente conectado, a partir um formulário de publicar em mural 
def criar_publicacao(formulario):

    # Cria uma nova publicação usando o modelo 'Publicacao'
    publicacao = Publicacao(
    titulo=formulario.titulo.data,
    conteudo=formulario.conteudo.data,
    idioma=formulario.idioma,
    autor=current_user._get_current_object()
    )

    # Imprime o id das tags selecionadas
    # formulario.tags.data retorna o id das tags selecionadas
    print(formulario.tags.data)

    # Para cada tag selecionada no formulário
    for tag in formulario.tags.data:

        # Seleciona a tag no banco de dados de acordo com o que foi selecionado
        t = Tag.query.filter_by(id=tag).first()

        # Adiciona a tag selecionada à lista de tags da publicação
        publicacao.tags.append(t)

    # Retorna o objeto que representa a publicação
    return publicacao



