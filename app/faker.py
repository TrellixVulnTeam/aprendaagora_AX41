from random import randint, choice
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .modelos import (
    Role,
    Permissao,
    Usuario,

    Publicacao,
    Tag,
    Comentario,

    Materia,
    Curso,
    Topico,
    Licao,
    Questao,

    Emblema,

    TopicoAmei,
    LicaoAmei,
    QuestaoAmei,
    PublicacaoAmei,
    ComentarioAmei
)

# Lista de palavras relacionadas a estudo de idiomas
lista_palavras = [
    'palavra', 'verbo', 'frase', 'difícil', 'conjugação',
    'pronúncia', 'inglês', 'escola', 'estudos', 'livro',
    'cultura', 'gramática', 'vocabulário', 'fácil', 'estudantes',
    'professor', 'exercício', 'prática', 'rápido', 'devagar', 'exterior',
    'sotaque', 'poliglota', 'idioma', 'língua', 'semântica', 'linguística',
    'literatura', 'expressão', 'linguagem', 'dialeto', 'fala', 'adjetivo',
    'dicionário', 'gíria'
]

lista_palavras_matematica = ['soma', 'adição', 'subtração', 'divisão', 'multiplicação', 'quociente', 'fração', 'geometria', 'trigonometria']

lista_palavras_biologia = ['fotossíntese', 'orgão', 'planta', 'semente', 'caule', 'sistema nervoso', 'sistema digestivo']

lista_palavras_quimica = ['reação', 'átomo', 'molécula', 'explosão']

lista_palavras_fisica = []

lista_palavras_historia = ['guerra', 'comércio', 'colonização', 'governo', 'Estado']

lista_palavras_geografia = ['terreno', 'escavação', 'bioma']

lista_palavras_filosofia = ['sofismo', 'metafísica']

lista_palavras_sociologia = ['sociedade']

lista_palavras_arte = ['tinta', 'barroco']

lista_palavras_materias = [
    {
        'ingles': lista_palavras
    },
    {
        'espanhol': lista_palavras
    },
    {
        'frances': lista_palavras
    },
    {
        'italiano': lista_palavras
    },
    {
        'alemao': lista_palavras
    },
    {
        'japones': lista_palavras
    },
    {
        'chines': lista_palavras
    },
    {
        'portugues': lista_palavras
    },
    {
        'matematica': lista_palavras
    },
    {
        'biologia': lista_palavras
    },
    {
        'quimica': lista_palavras
    },
    {
        'fisica': lista_palavras
    },
    {
        'biologia': lista_palavras
    },
    {
        'historia': lista_palavras
    },
    {
        'geografia': lista_palavras
    },

    {
        'filosofia': lista_palavras
    },
    {
        'sociologia': lista_palavras
    },
    {
        'arte': lista_palavras
    },
]



"""

#   # ##### ####  ##### #     ##### ##### 
## ## #   # #   # #     #     #   # #     
# # # #   # #   # ##### #     #   # ##### 
#   # #   # #   # #     #     #   #     # 
#   # ##### ####  ##### ##### ##### ##### 

"""

def usuarios(n_usuarios=20):

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Repita 'n_usuarios' vezes
    for i in range(n_usuarios):

        nome_usuario = fake.user_name()
        email = fake.email()

        # Se já ouver um usuário com o nome gerado
        if (Usuario.query.filter_by(nome_usuario=nome_usuario).first() or Usuario.query.filter_by(email=email).first()):
            continue
        else:

            # Cria um usuário fake
            u = Usuario(
                    email=email,

                    nome_usuario=fake.user_name(),
                    
                    senha='password',
                    
                    confirmado=True,
                    
                    nome=fake.name(),
                    
                    sobrenome=fake.name(),
                    
                    localizacao=fake.city(),
                    
                    sobre=fake.sentence(),
                    
                    membro_desde=fake.past_date()
                )

            # Adiciona o usuário à sessão
            db.session.add(u)

        try:
            # Salva usuários no banco de dados
            db.session.commit()

        except IntegrityError:

            # Reverte alterações
            db.session.rollback()
         

def cursos(n_cursos=50):


    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Seleciona todos os ids das matérias
    lista_ids_materias = [n for n in range(1, len(Materia.query.all()) + 1)]

   
    # Seleciona as palavras relacionadas à matéria
    #palavras = lista_palavras_materias[materia_id_escolhido]
    palavras = lista_palavras

    for i in range(n_cursos):

        # Seleciona um id aleatório
        materia_id_escolhido = choice(lista_ids_materias)

        nivel = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        c = Curso(
            materia_id=materia_id_escolhido,
            instrutor_id=1,
            nome=fake.sentence(nb_words=5, ext_word_list=palavras).capitalize(),
            descricao=fake.sentence(nb_words=20, ext_word_list=palavras).capitalize(),
            nivel=nivel,
            nome_foto="placeholder.jpg"
        )

        # Adiciona o usuário à sessão
        db.session.add(c)
        
    try:
        # Salva usuários no banco de dados
        db.session.commit()

    except IntegrityError:

        # Reverte alterações
        db.session.rollback()


def topicos(n_topicos=100):

    """
        id
        titulo
        descricao
        nome_foto
        curso_id
        materia_id
        licoes
        comentarios
        ameis
    """

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')


    # Seleciona todos os ids das matérias
    lista_ids_cursos = [n for n in range(1, len(Curso.query.all()) + 1)]


    # Seleciona as palavras relacionadas à matéria
    # palavras = lista_palavras_materias[materia_id_escolhido]
    palavras = lista_palavras


    for i in range(n_topicos):

        curso_id_escolhido = choice(lista_ids_cursos)

        curso = Curso.query.filter_by(id=curso_id_escolhido).first()

        materia_id = curso.materia.id

        t = Topico(
            titulo=fake.sentence(nb_words=5, ext_word_list=palavras).capitalize(),
            descricao=fake.sentence(nb_words=20, ext_word_list=palavras).capitalize(),
            nome_foto="placeholder.jpg",
            curso_id=curso_id_escolhido,
            materia_id=materia_id
        )

        # Adiciona o usuário à sessão
        db.session.add(t)
        
    try:
        # Salva usuários no banco de dados
        db.session.commit()

    except IntegrityError:

        # Reverte alterações
        db.session.rollback()


def licoes(n_licoes=200):
    

    """
        id
        titulo
        subtitulo
        conteudo
        conteudo_html
        nome_foto
        n_palavras
        data
        autor_id
        topico_id
        curso_id
        materia_id
    """

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')


    # Seleciona todos os ids dos tópicos
    lista_ids_topicos = [n for n in range(1, len(Topico.query.all()) + 1)]


    # Seleciona as palavras relacionadas ao tópico
    # palavras = lista_palavras_materias[materia_id_escolhido]
    palavras = lista_palavras


    for i in range(n_licoes):

        topico_id_escolhido = choice(lista_ids_topicos)

        topico = Topico.query.filter_by(id=topico_id_escolhido).first()

        curso_id = topico.curso.id

        materia_id = topico.materia.id
        
        l = Licao(
            titulo=fake.sentence(nb_words=5, ext_word_list=palavras).capitalize(),
            subtitulo=fake.sentence(nb_words=5, ext_word_list=palavras).capitalize(),
            conteudo=fake.sentence(nb_words=100, ext_word_list=palavras).capitalize(),
            nome_foto="placeholder.jpg",
            autor_id=1,
            topico_id=topico_id_escolhido,
            curso_id=curso_id,
            materia_id=materia_id,
        )

        # Adiciona o usuário à sessão
        db.session.add(l)
        
    try:
        # Salva usuários no banco de dados
        db.session.commit()

    except IntegrityError:

        # Reverte alterações
        db.session.rollback()


def questoes(n_licoes):
    return 1


def publicacoes(n_publicacoes=100): 

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Define o número de usuários cadastrados no sistema
    n_usuarios = Usuario.query.count()

    # Repita 'n_publicacoes' vezes
    for i in range(n_publicacoes):

        # Seleciona um usuário de forma aleatória
        u = Usuario.query.offset(randint(0, n_usuarios - 1)).first()

        # Cria um publicação com dados aleatórios
        p = Publicacao(
            titulo=fake.sentence(nb_words=5, ext_word_list=lista_palavras).capitalize(),
            subtitulo=fake.sentence(nb_words=5, ext_word_list=lista_palavras).capitalize(),
            conteudo=fake.sentence(nb_words=100, ext_word_list=lista_palavras).capitalize(),
            data_criacao=fake.past_date(),
            autor=u,
            idioma='ingles',
            nome_foto="placeholder.jpg"
        )

        # Repita 2 vezes
        for i in range(2):

            # Define 'id_aleatorio' de forma aleatória
            id_aleatorio = randint(1, 4)

            # Seleciona a tag no banco de dados de acordo com id aleatório criado
            t = Tag.query.filter_by(id=id_aleatorio).first()

            # Adiciona a tag aleatória à lista de tags da publicação
            p.tags.append(t)
    
        # Adiciona a publicação à sessão
        db.session.add(p)
    
    try:
        # Salva publicações no banco de dados
        db.session.commit()

    except IntegrityError:
        # Reverte alterações
        db.session.rollback()


def artigos(n_artigos=50):
    return 1



"""

#   # ##### #   #  ###  ##### ##### ##### 
#   # #     #   # ## ## #   #   #   #   # 
#   # ##### #   # #   # #####   #   #   # 
#   #     # #   # ##### #  #    #   #   # 
##### ##### ##### #   # #   # ##### ##### 

"""


def seguir(n_seguir=100):
    return 1


def usuarios_materias():
    return 1

def usuarios_cursos():
    return 1

def usuarios_topicos():
    return 1

def usuarios_licoes():
    return 1

def usuarios_emblemas():
    return 1


"""

##### ##### #   # ##### #   # #####  ###  ##### ##### ##### 
#     #   # ## ## #     ##  #   #   ## ## #   #   #   #   # 
#     #   # # # # ##### # # #   #   #   # #####   #   #   # 
#     #   # #   # #     #  ##   #   ##### #  #    #   #   # 
##### ##### #   # ##### #   #   #   #   # #   # ##### ##### 

"""

def comentarios_cursos(n_comentarios=10):
    return 1


def comentarios_topicos(n_topicos=100):
    return 1


# Cria comentários em publicações
def comentarios_publicacoes(n_comentarios=1000):

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Seleciona os ids das publicações existentes
    ids_publicacoes = [id for id, in db.session.query(Publicacao.id)]

    # Seleciona os ids dos usuários existentes
    ids_usuarios = [id for id, in db.session.query(Usuario.id)]

    """
    Link da solução:
    https://stackoverflow.com/questions/48466959/query-for-list-of-attribute-instead-of-tuples-in-sqlalchemy

    ids_publicacoes = db.session.query(Publicacao.id).all()

    print(ids_publicacoes)

    for id in ids_publicacoes:

        print(id[0])
    """


    # Repita 'n_comentarios' vezes
    for i in range(n_comentarios):
        
        # Cria um comentário com conteúdo, autor e publicação aleatórios
        c = Comentario(

            # 'choice()' é uma função da biblioteca 'random' que escolhe um elemento aleatório em um vetor

            publicacao_id=choice(ids_publicacoes),

            autor_id=choice(ids_usuarios),

            conteudo=fake.sentence(nb_words=20, ext_word_list=lista_palavras).capitalize()
        )

        # Adiciona o comentário à sessão
        db.session.add(c)
    

    try:
        # Salva comentários no banco de dados
        db.session.commit()
    except IntegrityError:
        # Reverte alterações
        db.session.rollback()


def comentarios_artigos():
    return 1


def comentarios_licoes(n_comentarios):
    return 1


def comentarios_questoes(n_comentarios):
    return 1


"""

 ###  #   # ##### ##### ##### 
## ## ## ## #       #   #     
#   # # # # #####   #   ##### 
##### #   # #       #       # 
#   # #   # ##### ##### ##### 

"""

def ameis_comentarios():
    return 1

def ameis_publicacoes():
    return 1

def ameis_artigos():
    return 1

def ameis_licoes():
    return 1

def ameis_topicos():
    return 1

def ameis_cursos():
    return 1