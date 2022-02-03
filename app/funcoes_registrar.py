from flask_login import current_user

from .modelos import (
    Publicacao,
    Tag,
    Comentario,
    Usuario,
    Materia,
    Curso,
    Topico,
    Licao,
    Questao
)

from . import db


def registrar_curso(formulario, nome_foto):
    
    # Seleciona o id da matéria a partir do nome simples
    materia_id = Materia.query.filter_by(nome_simples=formulario.materia.data).first().id

    # Seleciona o id do instrutor a partir do nome de usuário
    instrutor_id = Usuario.query.filter_by(nome_usuario=formulario.instrutor.data).first().id
    

    # Cria o curso
    curso = Curso(
        materia_id=materia_id,
        instrutor_id=instrutor_id,
        nome=formulario.nome.data,
        descricao=formulario.descricao.data,
        nivel=formulario.nivel.data,
        nome_foto=nome_foto
    )
    

    return curso


def registrar_topico(formulario, nome_foto):

    materia_id = Materia.query.filter_by(nome_simples=formulario.materia.data).first().id

    topico = Topico(
        titulo=formulario.titulo.data,
        descricao=formulario.descricao.data,
        nome_foto=nome_foto,
        materia_id=materia_id,
        curso_id=formulario.curso.data
    )

    return topico


def registrar_licao(formulario, nome_foto):

    materia = formulario.materia.data

    materia_id = Materia.query.filter_by(nome_simples=materia).first().id


    print("Título: ", formulario.titulo.data)
    print("Subtítulo: ", formulario.subtitulo.data)
    print("Conteúdo: ", formulario.conteudo.data)
    print("Nome foto: ", nome_foto)
    print("Autor: ", current_user._get_current_object())
    print("Tópico ID: ", formulario.topico.data)
    print("Curso ID: ", formulario.curso.data)
    print("Materia ID: ", materia_id)


    """ 

        Erro:  super(type, obj): obj must be an instance or subtype of type

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    """
    licao = Licao(
        titulo=formulario.titulo.data,
        subtitulo=formulario.subtitulo.data,
        conteudo=formulario.conteudo.data,
        nome_foto=nome_foto,
        autor=current_user._get_current_object(),
        topico_id=int(formulario.topico.data),
        curso_id=int(formulario.curso.data),
        materia_id=materia_id
    )

    return licao
    

def registrar_questao(formulario):

    """
        titulo
        enunciado
        opcaoa
        opcaob
        opcaoc
        opcaod
        opcaoe
        explicacao
        autor_id

        materia_id
        curso_id
        topico_id
    
        tipo

        ano
        prova
        dia
        tags
    """

    questao = Questao(
        titulo=formulario.titulo.data,
        enunciado=formulario.enunciado.data,
        opcaoa=formulario.opcaoa.data,
        opcaob=formulario.opcaob.data,
        opcaoc=formulario.opcaoc.data,
        opcaod=formulario.opcaod.data,
        opcaoe=formulario.opcaoe.data,
        explicacao=formulario.explicacao.data,
        autor=current_user._get_current_object(),

        materia_id=formulario.materia.data,
        curso_id=formulario.curso.data,
        topico_id=formulario.topico.data,
    
        enem=formulario.enem.data,

        ano=formulario.ano.data,
        prova=formulario.prova.data,
        dia=formulario.dia.data,
    )

    """
    # Para cada tag selecionada no formulário
    for tag in formulario.tags.data:

        # Seleciona a tag no banco de dados de acordo com o que foi selecionado
        t = Tag.query.filter_by(id=tag).first()

        # Adiciona a tag selecionada à lista de tags da questão
        questao.tags.append(t)
    """
    
    return questao


# Esta função cria uma publicação após receber um pedido POST, de um cliente conectado, a partir um formulário de publicar em mural 
def registrar_publicacao(formulario):

    # Cria uma nova publicação usando o modelo 'Publicacao'
    publicacao = Publicacao(
        titulo=formulario.titulo.data,
        conteudo=formulario.conteudo.data,
        idioma=formulario.idioma,
        autor=current_user._get_current_object()
    )

    # Para cada tag selecionada no formulário
    for tag in formulario.tags.data:

        # Seleciona a tag no banco de dados de acordo com o que foi selecionado
        t = Tag.query.filter_by(id=tag).first()

        # Adiciona a tag selecionada à lista de tags da publicação
        publicacao.tags.append(t)

    # Retorna o objeto que representa a publicação
    return publicacao


# A função registrar_artigo() é igual à funcão registrar_publicacao(), entretanto não define um idioma da publicação
def registrar_artigo(formulario, nome_foto):

    n_palavras = len(formulario.conteudo.data.split())

   
    print("\n\nLOG\n\n")
    print(n_palavras)
    print("\n\nFIM LOG\n\n")

    print(formulario.titulo.data)
    print(formulario.subtitulo.data)
    print(formulario.conteudo.data)
    print(nome_foto)

    
    artigo = Publicacao(

        titulo = formulario.titulo.data,
        subtitulo = formulario.subtitulo.data,
        conteudo=formulario.conteudo.data,
        nome_foto=nome_foto,
        autor=current_user._get_current_object(),
        n_palavras=n_palavras
    )

    print(formulario.tags.data)

    for tag in formulario.tags.data:

        # Seleciona a tag no banco de dados de acordo com o que foi selecionado
        t = Tag.query.filter_by(id=tag).first()

        # Adiciona a tag selecionada à lista de tags da publicação
        artigo.tags.append(t)

    return artigo
    
    
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

