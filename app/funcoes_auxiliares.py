from flask_login import current_user
from .modelos import Publicacao, Tag, Comentario
from . import db

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


# Cria um comentário em uma publicação
def registrar_comentario(publicacao_id, autor_id, conteudo):

    # Cria um novo comentário
    novo_comentario = Comentario(

            publicacao_id=publicacao_id,
            autor_id=autor_id,
            conteudo=conteudo
    )

    # Adiciona comentário à sessão
    db.session.add(novo_comentario)

    # Salva alterações no banco de dados
    db.session.commit()


# Limita a quantidade de caracteres de uma string em 200 caracteres
def truncar_texto(texto):

    # Se a string possuir mais de 200 caracteres
    if len(texto) > 200:
        
        # Fatie os primeiros 200 caracteres da string e adicione "..." no final
        texto = texto[0:200] + '...'

    # Retorne a string truncado
    return texto
